#
# Author: Robert Patel
# This class represents the controller for the dashboard GUI.
#
from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QToolTip, QMainWindow, QTableWidgetItem, QInputDialog
from services.auth_service import AuthService
from services.db_service import DatabaseService
from services.app_state import AppState
from PyQt6 import QtGui, QtCore
from controllers.portfolio_controller import PortfolioController
from PyQt6.QtGui import QDesktopServices, QCursor
from PyQt6.QtCore import QUrl
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from datetime import datetime
import yfinance as yf


class DashboardController:
    def __init__(self, ui, main_window: QMainWindow, db_service: DatabaseService, auth_service: AuthService, app_state: AppState, screen_manager, user_controller, portfolio_controller):
        super().__init__()
        self.ui = ui
        self.main_window = main_window
        self.db_service = db_service
        self.auth_service = auth_service
        self.app_state = app_state
        self.screen_manager = screen_manager
        self.user_controller = user_controller
        self.portfolio_controller = portfolio_controller
        self._pie_view = None
        
        # pie chart plumbing
        self._pie_view = None
        layout = self.ui.pieChartContainer.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.pieChartContainer)
            layout.setContentsMargins(0, 0, 0, 0)
        self._pie_layout = layout

        self.setup_connections()

    # Sets up the connections used within the class.
    def setup_connections(self):
        self.ui.btnHome.clicked.connect(self.handle_home)
        self.ui.btnDashboard.clicked.connect(self.load_portfolio)
        self.ui.btnAddHolding.clicked.connect(self.handle_add_stock)
        self.ui.btnSellHolding.clicked.connect(self.handle_sell_stock)
        self.ui.btnAbout.clicked.connect(self.handle_about)
        self.ui.btnGitHub.clicked.connect(self.handle_github)
        self.ui.btnLinkedIn.clicked.connect(self.handle_linkedin)
        self.ui.btnAddWatchlist.clicked.connect(self.handle_add_watchlist_ticker)
        self.ui.btnAnalyze.clicked.connect(
            lambda: self.load_recommendations(self.ui.txtTickerAnalyzer.text())
            )

    # Loads the users portfolio from the class.
    def load_portfolio(self):
        user = self.app_state.get_current_user()
        if not user:
            return

        user_email = user.get_email()
        user_id = self.db_service.get_user_id(user_email)
        portfolio_id = self.db_service.get_portfolio_id(user_id)

        # --- 1) get holdings: ticker -> quantity --------------------------------
        holdings = self.db_service.get_tickers(portfolio_id) or []

        # normalize into a list of (ticker, quantity)
        if isinstance(holdings, dict):
            items = [(str(t).upper(), float(q or 0)) for t, q in holdings.items()]
        else:  # assume list of dicts [{'ticker':..., 'quantity':...}]
            items = [(str(h.get("ticker","")).upper(), float(h.get("quantity") or 0)) for h in holdings]

        # --- 2) fill the table ---------------------------------------------------
        table = self.ui.tblPortfolio
        table.setRowCount(len(items))

        value_by_ticker = {}

        for row_index, (ticker, shares) in enumerate(items):
            if not ticker or shares <= 0:
                # fill row with N/A and continue
                for col_index, v in enumerate([ticker or "N/A", "N/A", "0", "N/A", "N/A", ""]):
                    table.setItem(row_index, col_index, self.make_table_item(str(v)))
                continue

            current_price = float(self.portfolio_controller.get_current_price(ticker) or 0.0)

            # If you still want Gain/Loss, you need a buy price.
            # Option A: have get_tickers() also return buy_price
            # Option B: fetch per-ticker avg buy price from DB:
            buy_price = self.db_service.get_avg_buy_price(portfolio_id, ticker)  # implement this; see SQL below

            # Format cells
            entry_str   = "N/A" if buy_price is None else f"${float(buy_price):.2f}"
            curr_str    = f"${current_price:,.2f}"
            shares_str  = f"{int(shares):d}"

            if buy_price is None:
                gl_str = "N/A"
            else:
                gl = shares * (current_price - float(buy_price))
                gl_str = f"${gl:,.2f}"

            # Ticker | Entry Price | Shares | Current Price | Gain/Loss | Recommendation
            row_values = [ticker, entry_str, shares_str, curr_str, gl_str, ""]
            for col_index, v in enumerate(row_values):
                table.setItem(row_index, col_index, self.make_table_item(str(v)))

            # accumulate for pie/total
            value_by_ticker[ticker] = value_by_ticker.get(ticker, 0.0) + shares * current_price

        # Displays the totals value of the portfolio.
        total = sum(value_by_ticker.values())
        self.ui.txtPortfolioTotal.setText(f"${total:,.2f}")

        # Displays the total profit for the portfolio.
        profit = self.db_service.get_portfolio_profit(portfolio_id) or 0.0
        self.ui.txtTotalProfit.setText(f"${profit:,.2f}")

        # --- 4) (optional) draw/update pie if you added the helper earlier -------
        if hasattr(self, "_render_pie"):
            slices = [(t, v) for t, v in value_by_ticker.items() if v > 0]
            self._render_pie(slices or [("No Data", 1.0)])

            # Loads the portfolio value into the designated textbox.
            total = self.db_service.get_portfolio_value(portfolio_id) or 0.0
            self.ui.txtPortfolioTotal.setText(f"${total:,.2f}")

            # Loads the portfolios current total profit.
            current_total = self.db_service.get_portfolio_profit(portfolio_id) or 0.0
            self.ui.txtTotalProfit.setText(f"${current_total:,.2f}")

    # Loads the recommendations into the corresponding table.
    def load_recommendations(self, ticker: str | None = None):
        # Prefer the passed-in ticker; otherwise read from the analyzer field.
        if ticker is None:
            if hasattr(self.ui, "txtTickerAnalyzer"):
                ticker = self.ui.txtTickerAnalyzer.text().strip()
            else:
                self.show_error("Invalid Input", "Ticker field not found in the UI.")
                return
        else:
            ticker = str(ticker).strip()

        if not ticker:
            self.show_error("Invalid Input", "Please enter a ticker symbol.")
            return

        # If an analysis controller exists, try to open the analysis page
        try:
            if hasattr(self, "analysis_controller") and self.analysis_controller is not None:
                self.analysis_controller.load_analysis(ticker)
                self.screen_manager.show_analysis()
        except ValueError as e:
            self.show_error("Invalid Ticker", str(e))
            return
        except Exception as e:
            self.show_error("Error", f"An unexpected error occurred: {str(e)}")
            return

        # Pull indicators and recommendations
        try:
            price_data = self.portfolio_controller.get_price_data(ticker)

            # Indicators -> tblIndicators
            indicators = [
                self.portfolio_controller.get_ema(price_data, 10),
                self.portfolio_controller.get_ema(price_data, 34),
                self.portfolio_controller.get_ema(price_data, 50),
                self.portfolio_controller.get_sma(price_data, 20),
                self.portfolio_controller.get_sma(price_data, 50),
                self.portfolio_controller.get_sma(price_data, 100),
                self.portfolio_controller.get_sma(price_data, 200),
                self.portfolio_controller.get_adx(price_data),
                self.portfolio_controller.get_rsi(price_data),
                self.portfolio_controller.get_rsi_volume(price_data),
            ]

            for row, value in enumerate(indicators):
                try:
                    display_value = f"{float(value):.2f}"
                except (ValueError, TypeError):
                    display_value = str(value)
                self.ui.tblIndicators.setItem(row, 0, QTableWidgetItem(display_value))

            # Recommendations -> tblTechnicalAnalysis
            recommendations = [
                self.portfolio_controller.get_datetime(),
                self.portfolio_controller.is_golden_cross(ticker, price_data),
                self.portfolio_controller.get_short_momentum(price_data),
                self.portfolio_controller.is_price_over_200_ema(price_data),
                self.portfolio_controller.get_rsi_strength(price_data),
                self.portfolio_controller.is_rsi_oversold(price_data),
                self.portfolio_controller.is_adx_strong(price_data),
                self.portfolio_controller.pullback_opportunity(ticker, price_data),
                self.portfolio_controller.volume_spike(price_data),
                self.portfolio_controller.high_volume(price_data),
            ]

            table = self.ui.tblTechnicalAnalysis
            row_idx = table.rowCount()
            table.insertRow(row_idx)

            for col_idx, value in enumerate(recommendations):
                item = QTableWidgetItem(str(value))

                # Conditional coloring
                val_str = str(value).lower()
                if val_str in ["true", "bullish", "yes"]:
                    item.setBackground(QtGui.QColor("lightgreen"))
                elif val_str in ["false", "bearish", "no"]:
                    item.setBackground(QtGui.QColor("lightcoral"))

                table.setItem(row_idx, col_idx, item)

        except ValueError as e:
            self.show_error("Invalid Ticker", f"Ticker '{ticker}' is not valid. {str(e)}")
        except Exception as e:
            self.show_error("Error", f"Unexpected error while analyzing '{ticker}': {str(e)}")

    # Opens the home window for a logged-in user.
    def handle_home(self):
        self.screen_manager.show_home_logged_in()

    # Opens the window to prompt the user to buy/add a stock to their portfolio.
    def handle_add_stock(self):
        self.screen_manager.show_buy_window()

    # Opens the window to prompt the user to sell a stock.
    def handle_sell_stock(self):
        self.screen_manager.show_sell_window()

    # Opens the user / settings window.
    def handle_usersettings(self):
        None
        # IN PROGRESS

    # Opens the github profile.
    def handle_github(self):
        url = "https://github.com/robertpatel28"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    # Opens the linkedin profile.
    def handle_linkedin(self):
        url = "https://www.linkedin.com/in/robertpatel/"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)

    def handle_about(self):
        url = "https://github.com/robertpatel28/BuddyTrade"
        opened = QDesktopServices.openUrl(QUrl(url))
        if not opened:
            # Fallback to Python's webbrowser if Qt fails
            import webbrowser
            webbrowser.open(url)
    def handle_add_watchlist_ticker(self):

        # Prompt user for input
        ticker, ok = QInputDialog.getText(self.main_window, "Add to Watchlist", "Enter ticker symbol:")
        
        if not ok or not ticker.strip():
            return  # Cancelled or empty

        ticker = ticker.strip().upper()

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Validate shortName and currentPrice
            name = info.get("shortName")
            price = info.get("currentPrice") or info.get("regularMarketPrice")

            if not name or price is None:
                raise ValueError("Invalid ticker")

            # Add to watchlist table
            row_idx = self.ui.tblWatchlist.rowCount()
            self.ui.tblWatchlist.insertRow(row_idx)
            self.ui.tblWatchlist.setItem(row_idx, 0, QTableWidgetItem(ticker))
            self.ui.tblWatchlist.setItem(row_idx, 1, QTableWidgetItem(name))
            self.ui.tblWatchlist.setItem(row_idx, 2, QTableWidgetItem(f"${float(price):.2f}"))

        except Exception:
            QMessageBox.critical(self.main_window, "Invalid Ticker", f"'{ticker}' is not a valid stock ticker.")

    # Adds value to a table.
    def make_table_item(self, value: str) -> QTableWidgetItem:
        return QTableWidgetItem(value)
    
    # Helper method that shows error box with given title and message.
    def show_error(self, title, message):
        QMessageBox.warning(self.main_window, title, message)

    # Helper method that shows information box with given title and message.
    def show_info(self, title, message):
        QMessageBox.information(self.main_window, title, message)

    # Renders the pie chart.
    def _render_pie(self, slices: list[tuple[str, float]]):
        """
        slices: [('AAPL', 1356.06), ('SPY', 1276.22), ...]
        Renders into self.ui.pieChartContainer with hover tooltips only (no labels/leader lines).
        """
        # Ensure the container has a layout
        layout = self.ui.pieChartContainer.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.pieChartContainer)
            layout.setContentsMargins(0, 0, 0, 0)

        # Remove previous chart view
        if getattr(self, "_pie_view", None):
            layout.removeWidget(self._pie_view)
            self._pie_view.deleteLater()
            self._pie_view = None

        # Clean data
        data = [(str(name).strip() or "Unknown", max(0.0, float(val or 0)))
                for name, val in (slices or [])]
        if not data:
            data = [("No Data", 1.0)]
        total = sum(v for _, v in data) or 1.0

        # Build series (no labels -> no leader lines)
        series = QPieSeries()
        for name, value in data:
            series.append("", value)  # empty label text

        # Hide labels completely
        series.setLabelsVisible(False)
        for s in series.slices():
            s.setLabelVisible(False)
            s.setLabel("")  # ensure blank

        # Remove slice borders
        no_pen = QtGui.QPen()
        no_pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        for s in series.slices():
            s.setPen(no_pen)

        # Chart
        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        series.setPieSize(0.92)                      # big pie (no labels to make room for)
        chart.setMargins(QtCore.QMargins(2, 2, 2, 2))
        chart.legend().setVisible(False)

        # Hover tooltip (full text on hover)
        def on_hover(slice_obj, state: bool):
            if not state:
                QToolTip.hideText()
                return
            try:
                idx = series.slices().index(slice_obj)
            except ValueError:
                return
            name, value = data[idx]
            pct = value / total
            QToolTip.showText(
                QtGui.QCursor.pos(),
                f"{name}: ${value:,.2f} ({pct:.1%})",
                self.ui.pieChartContainer
            )

        series.hovered.connect(on_hover)

        # Mount view
        view = QChartView(chart)
        view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        layout.addWidget(view)
        self._pie_view = view
