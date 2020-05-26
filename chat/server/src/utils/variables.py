import logging

CONSTS = {
    "encoding": "utf8",
    "default-ip": "127.0.0.1",
    "default-port": 7777,
    "max-connections": 5,
    "max-pack_len": 2540000,
    "logging_level": logging.DEBUG,
    "jim": {
        "action": "action",
        "time": "time",
        "user": "user",
        "account": "account_name",
        "sender": "sender",
        "destination": "to",
        "pubkey": "pubkey",
        "passhash": "passhash",
        "keys": {
            "presence": "presence",
            "responce": "responce",
            "reg": "registration",
            "get_contacts": "get_contacts",
            "add_contact": "add_contact",
            "del_contact": "del_contact",
            "get_avatar": "get_avatar",
            "add_avatar": "add_avatar",
            "req_pubkey": "req_pubkey",
            "error": "error",
            "data": "bin",
            "resp_default_ip": "responce_default_adress",
            "message": "message",
            "message_text": "msg_text",
            "exit": "exit"
        }
    }
}

RESPONCES = {
    "resp_200": {CONSTS["jim"]["keys"]["responce"] : 200},
    "resp_202": {CONSTS["jim"]["keys"]["responce"] : 202},
    "resp_400": {
        CONSTS["jim"]["keys"]["responce"] : 400,
        CONSTS["jim"]["keys"]["error"]: None
    },
    "resp_511": {
        CONSTS["jim"]["keys"]["responce"] : 511,
        CONSTS["jim"]["keys"]["data"]: None        
    }
}