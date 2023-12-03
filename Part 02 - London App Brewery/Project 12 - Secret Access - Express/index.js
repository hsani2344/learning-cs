import { dirname } from "path";
import { fileURLToPath } from "url";
import express from "express";
import bodyParser from "body-parser";

const app = express();
const port = 3000;
const __dirname = dirname(fileURLToPath(import.meta.url));

const homepage = __dirname + "/public/index.html";

app.use(bodyParser.urlencoded({extended: true}));

app.get("/", (req, res) => {
  res.sendFile(homepage);
})

app.post("/check", (req, res) => {
  if (req.body.password == 'ILoveProgramming') {
    res.sendFile(__dirname + "/public/secret.html");
  }
  else {
    res.sendFile(homepage)
  }
})

app.listen(port, (req, res) => {
  console.log(`Listening on port ${port}`);
})
