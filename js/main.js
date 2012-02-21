
radiohead_quotes = [
  "Don't talk politics and don't throw stones Your royal highnesses",
  "It's not like the movies They fed us on little white lies",
  "Clothes are on the lawn with the furniture",
  ]
horse_ebooks_quotes = [
  "Your computer and your golf clubs are your best friends.",
  "Well imagine how it s going to feel when the next guy who comes along starts smack talking you, and then you utterly destroy",
  "walk into your house and see a new chair",
  ]

function get_quote() {
  if (Math.random() < .5) {
    var index = Math.floor(Math.random() * radiohead_quotes.length);
    return radiohead_quotes[index];
  } else {
    var index = Math.floor(Math.random() * horse_ebooks_quotes.length);
    return horse_ebooks_quotes[index];
  }
}
