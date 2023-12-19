import express from "express";
import db from 'pg';

const app = express();
const port = 3000;
const client = new db.Client({
  host: 'localhost',
  port: 5432,
  database: 'permalist',
  user: 'postgres',
  password: '123456',
})
await client.connect()

app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));

app.get("/", async (req, res) => {
  let items = await client.query({
      name: 'getItems',
      text: 'SELECT id, title FROM items'
    });
  res.render("index.ejs", {
    listTitle: "Today",
    listItems: items.rows,
  });
});

app.post("/add", async (req, res) => {
  const item = req.body.newItem;
  await client.query({
    name: 'addItem',
    text: 'INSERT INTO items(title) VALUES ($1)',
    values: [`${item}`]
  });
  res.redirect("/");
});

app.post("/edit", async (req, res) => {
  const itemId = req.body.updatedItemId;
  const updatedItemTitle = req.body.updatedItemTitle;
  client.query({
    name: 'updateItem',
    text: 'UPDATE items SET title = $1 WHERE id = $2',
    values: [`${updatedItemTitle}`, itemId]
  });
  res.redirect("/");

});

app.post("/delete", (req, res) => {
  const itemId = req.body.deleteItemId;
  client.query({
    name: 'itemId',
    text: 'DELETE FROM items WHERE id = $1',
    values: [itemId]
  });
  res.redirect("/");
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
