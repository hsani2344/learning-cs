import express from "express";
import ejs from "ejs";
import axios from "axios";

const app = express();
const port = 3000;
const API_URL = "https://secrets-api.appbrewery.com";

// app.use(express.urlencoded({extended: true}));
app.use(express.static("public"));

app.get("/", async (req, res) => {
  try {
    const result = await axios.get(API_URL + "/random");
    res.render("index.ejs", result.data);
  } catch (error) {
    res.send(JSON.stringify(error.response.data));
  }
});

app.listen(port, () => {
  console.log(`App listening to port ${port}`);
});

