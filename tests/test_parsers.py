from src.tennis_analytics.parsers import parse_competitions, parse_complexes, parse_rankings

def test_competition_json():
    cats, comps = parse_competitions({"competitions":[{"id":"c1","name":"Demo","type":"doubles",
        "gender":"men","category":{"id":"a1","name":"ATP"}}]})
    assert cats[0]["category_name"] == "ATP"
    assert comps[0]["competition_id"] == "c1"

def test_complex_json():
    xs, vs = parse_complexes({"complexes":[{"id":"x1","name":"Centre","venues":[
        {"id":"v1","name":"Court","city_name":"Patna","country_name":"India","timezone":"Asia/Kolkata"}]}]})
    assert xs[0]["complex_id"] == "x1"
    assert vs[0]["complex_id"] == "x1"

def test_ranking_json():
    players, ranks = parse_rankings({"rankings":[{"type":"doubles","competitor_rankings":[
        {"rank":1,"movement":0,"points":900,"competitions_played":8,
         "competitor":{"id":"p1","name":"Player","country":"India"}}]}]})
    assert players[0]["name"] == "Player"
    assert ranks[0]["points"] == 900
