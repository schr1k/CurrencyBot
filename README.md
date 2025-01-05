# Setup
1. Create virtual environment.
    ```bash  
    python -m venv venv  
    ```

2. Activate it.
    * On Windows:
        ```bash
        venv\Scripts\activate
        ```

    * On MacOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3. Install requirements.
    ```bash
    pip install -r requirements.txt
    ```

4. Create .env file.
    ```bash
    cp .env.example .env
    ```

# Launch
## Docker
### Development mode (fast-refresh)
```bash
docker compose watch
```

### Production mode
```bash
docker compose up --build -d
```

## Default
```bash
python main.py
```
