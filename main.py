from fastapi import FastAPI

app = FastAPI()


@app.get('/index')
def get_index():
    return {'data': '200'}
