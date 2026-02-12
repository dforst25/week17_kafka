from fastapi import FastAPI, status, HTTPException
import dal

app = FastAPI()


@app.get("/analytics/top-customers")
def get_top_customers():
    try:
        return dal.get_top_customers_by_orders()
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))

@app.get("/analytics/customers-without-orders")
def get_customers_with_zero_orders():
    try:
        return dal.get_customers_without_orders()
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/analytics/zero-credit-active-customers")
def get_customers_with_zero_credit():
    try:
        return dal.get_zero_credit_active_customers()
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
