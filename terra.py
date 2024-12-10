# import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

# create object/instance
app = FastAPI()
# to run it uvicorn latihan_api:app --reload in terminal

# create API Key
API_Key = "admin123"

# create endpoint home (semacam pintu gerbang)
@app.get("/")
def home():
    return {"message": "Mak Kau Hijau!!"}

# create endpoint data
@app.get("/data")
def read_data():
    # untuk read data csv
    df = pd.read_csv("data.csv")
    # harus ada return
    # bisa juga df.to_json
    return df.to_dict(orient="records")
    # convert dataframe ke dict dengan orient "records" setiap baris

# create endpoint data sesuai number id
@app.get("/data/{number_id}")
def read_item(number_id: int):
    # setiap endpoint harus membaca data lagi
    df = pd.read_csv("data.csv")
    # filter data by id
    filterData = df[df['id'] == number_id] #<---- dimasukkan dalam variabel

    # error handling, jika data empty
    if len(filterData) == 0:
        raise HTTPException(status_code=404, detail="Data gaada blok!!")

    return filterData.to_dict(orient="records") #<---- panggil variabelnya

@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    # create dictionary for updating data
    df = pd.read_csv("data.csv")
    # create dataframe from updated input
    updated_df = pd.DataFrame([{
        "id":number_id,
        "nama_barang": nama_barang,
        "harga":harga
    }])
    # updated_df = pd.DataFrame({
    #     "id":number_id,
    #     "nama_barang": nama_barang,
    #     "harga":harga
    # }, index = [0]) # <----- cara kedua, sama saja.

    # menggabungkan dataframe baru dengan yang lama
    df = pd.concat([df, updated_df], ignore_index=True)
    
    # save new 
    df.to_csv("data.csv", index=False)

    return {"message": f"Item with ID {number_id} has been updated successfully."}

@app.get("/secret")
def read_secret(api_key: str = Header(None)):
    secret_df = pd.read_csv("secret_data.csv")
    if api_key != API_Key or api_key == None:
        raise HTTPException(status_code=401, detail="MALING!!")

    return secret_df.to_dict(orient="records")