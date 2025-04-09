ktp_npwp_scanner/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI/Flask app entrypoint
│   ├── routes.py            # Endpoints for file upload and scan
│   ├── ocr_engine.py        # PaddleOCR wrapper
│   ├── parser_ktp.py        # Extract fields from KTP
│   ├── parser_CC.py         # Extract fields from Credit Card
│   ├── parser_npwp.py       # Extract fields from NPWP
│   └── utils.py             # Image preprocessing, helpers
│
├── samples/
│   └── sample_ktp.jpg
│   └── sample_npwp.jpg
│
├── requirements.txt
└── Dockerfile
