const express = require("express");
const app = express();
app.use(express.json());

const port = process.env.PORT || 8000;

async function chatbot(findStr) {
  let { NlpManager } = require("node-nlp"); //natural language processing for chatbot

  const manager = new NlpManager({
    languages: ["en"],
    nlu: { useNoneFeature: false },
    nlu: { log: false },
    forceNER: true,
    ner: { useDuckling: false },
  });

  manager.addCorpus("./corpus.json");
  await manager.train();
  manager.save();
  // manager.load();

  const result = await manager.extractEntities("en", findStr);
  console.log(result);
  let response = await manager.process("en", findStr);
  // console.log(response);
  return response.answer;
}

app.post("/api/bot", (req, res) => {
  res.set("Content-Type", "application/json");

  chatbot(req.body.msg).then(async (response) => {
    if (response == null) {
      res.status(200).json({ message: "sorry I did not understand." });
    } else {
      res.status(200).json({ message: response });
    }
  });
});

app.listen(port, () => {
  console.log("Server app listening on port " + port);
});
