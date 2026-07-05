from Trader_AngleOne import TraderAngleOne

crd = {
    "api_key"    : "abc",
    "secret_key" : "abc-abc-abc",
    "totp"       : "abcAKBDLEMI",
    "userid"     : "U8XX1XX",
    "pwd"        : "1XX8",
}

angle = TraderAngleOne(**crd)

# ------------------    THIS LIBRARY FETCH ONLY THE NSE - EQ DATA EG..{NIFTY,BANKNIFTY, RELIANCE, CIPLA etc..} NOT FUTURE DATA 

# GET 1_MIN RELIANCE DATA
reliance_1 = angle.get_history_data('RELIANCE','1','2026-01-01 9:15','2026-01-02 15:30','NSE')
# GET 3_MIN RELIANCE DATA
reliance_3 = angle.get_history_data('RELIANCE','3','2026-01-01 9:15','2026-01-02 15:30','NSE')
# GET 5_MIN RELIANCE DATA
reliance_5 = angle.get_history_data('RELIANCE','5','2026-01-01 9:15','2026-01-02 15:30','NSE')
# GET 15_MIN RELIANCE DATA
reliance_15 = angle.get_history_data('RELIANCE','15','2026-01-01 9:15','2026-01-02 15:30','NSE')
# GET 30_MIN RELIANCE DATA
reliance_30 = angle.get_history_data('RELIANCE','30','2026-01-01 9:15','2026-01-02 15:30','NSE')
# GET 1H_MIN RELIANCE DATA
reliance_1H = angle.get_history_data('RELIANCE','1H','2026-01-01 9:15','2026-01-02 15:30','NSE')
# GET 1D_MIN RELIANCE DATA
reliance_1D = angle.get_history_data('RELIANCE','1D','2026-01-01 9:15','2026-01-02 15:30','NSE')