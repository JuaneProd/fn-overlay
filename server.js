const express = require("express");
const socketio = require("socket.io");

const axios = require("axios");

const app = express();

app.set("views", __dirname + "/views");
app.set("view engine", "ejs");

app.use(express.json());

let observers = {
  zer0x: {
    url: "",
    key: "12341234",
  },
  Juane: {
    url: "",
    key: "1234",
  }
};

app.get("/widget/:observer", (req, res) => {
  res.render("widget", {
    urlWidget: observers[req.params.observer],
    observer: req.params.observer,
  });
});

app.post("/", (req, res) => {
  console.log("/: ", req.body);
});

app.get("/urlWidget/:observer", (req, res) => {
  res.send(observers[req.params.observer].url);
});

app.post("/urlWidget/:observer", async (req, res) => {
  if (req.body.key === observers[req.params.observer].key) {
    observers[req.params.observer].url = req.body.url;

    const headers = {
      headers: { "TRN-Api-Key": "d750f397-264f-4259-a8ac-f38d984aefaf" },
    };

    console.log(req.body.player);
    var playerName = req.body.player;
    console.log(playerName);

    const player = await axios
      .get(
        `https://api.fortnitetracker.com/v1/profile/pc/${playerName}`,
        headers
      )
      .catch((err) => {
        observers[req.params.observer].url =
          "https://trackercdn.com/cdn/fortnitetracker.com/icons/flags/globe.png";
        res.status(400).send("Unvalid player");
      });

    if (player.data.country) {
      observers[
        req.params.observer
      ].url = `https://cdn.thetrackernetwork.com/cdn/flags/4x3/${player.data.country}.svg`;

      res.status(200).send(observers[req.params.observer].url);
    } else {
      observers[req.params.observer].url =
        "https://trackercdn.com/cdn/fortnitetracker.com/icons/flags/globe.png";

      res.status(201).send(observers[req.params.observer].url);
    }
  } else {
    res.status(404).send("Invalid credentials!");
  }
});

const PORT = 8080;
const HOST = "localhost";

app.listen(process.env.PORT || 8080);
