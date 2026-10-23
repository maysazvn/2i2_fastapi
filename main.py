import logging
from math import prod

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySqlError

from database import executar_sql

app = FastAPI(title="FAST API 2INFO2")


@app.exception_handler(MySqlError)
def erro_de_banco(request: Request, exc: MySqlError):
    logging.getLogger("uvicorn.error").error("Erro no BD: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Nãof oi posivel acesar o BD"},
    )


def representar_produto(produto):
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "quantidade": produto["quantidade"],
        "preco": format(produto["preco"], "2f"),
    }


@app.get("/produtos")
def listar_produtos():
    sql = "SELECT * FROM produtos"
    produtos = executar_sql(sql)
    return {
        "dados": [representar_produto(produto) for produto in produtos],
        "sintaxesql": {"sql": sql, "parametros": []},
    }
