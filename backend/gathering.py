import facebook

graph = facebook.GraphAPI("CAACEdEose0cBAOrOuSotPSghjQa3EB8FdDlyNZCQHF85DIoBWtmaqsbql6lT"
                          "ZBxE7LCiZC0lAvduzI2FPia6MtnboNHVDpCaPOPT4ONFPz4IVmbRZA6SJ6zsW"
                          "JhTAhUiG6dfe7fKXFZAZC3KsZACLhvcjjVB9UrzbszYAUlyB7Ribbs2PedlAUP"
                          "fZBj7ZBZAYlHgn779TCHr9R7gZDZD")

profile = graph.get_object("me")
friends = graph.get_connections("me", "home")

