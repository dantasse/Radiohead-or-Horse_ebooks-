
radiohead_quotes = [
  "In an interstellar burst, I'm back to save the universe",
  "A pig in a cage on antibiotics",
  "Ice age coming, women and children first"
  ]
horse_ebooks_quotes = [
  "horse ebooks quote 1",
  "horse ebooks quote 2"
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
