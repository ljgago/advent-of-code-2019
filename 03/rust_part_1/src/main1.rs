//
// --- Day 3: Crossed Wires ---
//
// The gravity assist was successful, and you're well on your way to the Venus
// refuelling station. During the rush back on Earth, the fuel management system
// wasn't completely installed, so that's next on the priority list.
//
// Opening the front panel reveals a jumble of wires. Specifically, two wires
// are connected to a central port and extend outward on a grid. You trace the
// path each wire takes as it leaves the central port, one wire per line of
// text (your puzzle input).
//
// The wires twist and turn, but the two wires occasionally cross paths. To fix
// the circuit, you need to find the intersection point closest to the central
// port. Because the wires are on a grid, use the Manhattan distance for this
// measurement. While the wires do technically cross right at the central port
// where they both start, this point does not count, nor does a wire count as
// crossing with itself.
//
// For example, if the first wire's path is R8,U5,L5,D3, then starting from the
// central port (o), it goes right 8, up 5, left 5, and finally down 3:
//
// ...........
// ...........
// ...........
// ....+----+.
// ....|....|.
// ....|....|.
// ....|....|.
// .........|.
// .o-------+.
// ...........
//
// Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6,
// down 4, and left 4:
//
// ...........
// .+-----+...
// .|.....|...
// .|..+--X-+.
// .|..|..|.|.
// .|.-X--+.|.
// .|..|....|.
// .|.......|.
// .o-------+.
// ...........
//
// These wires cross at two locations (marked X), but the lower-left one is
// closer to the central port: its distance is 3 + 3 = 6.
//
// Here are a few more examples:
//
//     R75,D30,R83,U83,L12,D49,R71,U7,L72
//     U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
//     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
//     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
//
// What is the Manhattan distance from the central port to the closest intersection?

use std::env;
use std::fs;
use std::io::{prelude::*, BufReader};

#[derive(Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

fn up(point: Point, value: i32) -> Vec<Point> {
    let mut points: Vec<Point> = Vec::new();
    for y in 1..value {
        let p = Point {
            x: point.x,
            y: point.y + (1 + y),
        };
        points.push(p)
    }
    return points;
}

fn down(point: Point, value: i32) -> Vec<Point> {
    let mut points: Vec<Point> = Vec::new();
    for y in 1..value {
        let p = Point {
            x: point.x,
            y: point.y - (1 + y),
        };
        points.push(p)
    }
    return points;
}

fn right(point: Point, value: i32) -> Vec<Point> {
    let mut points: Vec<Point> = Vec::new();
    for x in 1..value {
        let p = Point {
            x: point.x + (1 + x),
            y: point.y,
        };
        points.push(p)
    }
    return points;
}

fn left(point: Point, value: i32) -> Vec<Point> {
    let mut points: Vec<Point> = Vec::new();
    for x in 1..value {
        let p = Point {
            x: point.x - (1 + x),
            y: point.y,
        };
        points.push(p)
    }
    return points;
}

fn distance_taxicab(origin: Point, destiny: Point) -> i32 {
    return (origin.x - destiny.x).abs() + (origin.y - destiny.y).abs();
}

fn calcule_points(input: String) -> Vec<Point> {
    let tracks: Vec<&str> = input.split(",").collect();
    let mut points: Vec<Point> = Vec::new();
    points.push(Point { x: 0, y: 0 });
    for track in tracks {
        let direccion: &str = &track[0..1];
        let value: i32 = String::from(&track[1..]).parse().unwrap();
        match direccion {
            "U" => {
                let last_point: Point = points.last().cloned().unwrap();
                let mut new_point = up(last_point, value);
                points.append(&mut new_point);
            }
            "D" => {
                let last_point: Point = points.last().cloned().unwrap();
                let mut new_point = down(last_point, value);
                points.append(&mut new_point);
            }
            "R" => {
                let last_point: Point = points.last().cloned().unwrap();
                let mut new_point = right(last_point, value);
                points.append(&mut new_point);
            }
            "L" => {
                let last_point: Point = points.last().cloned().unwrap();
                let mut new_point = left(last_point, value);
                points.append(&mut new_point);
            }
            _ => unreachable!(),
        };
    }
    return points;
}

fn calcule_min_distance(points: Vec<Point>) -> i32 {
    let origin = Point { x: 0, y: 0 };
    let mut min_distance: i32 = distance_taxicab(origin, points.clone()[1]);
    println!("Firts intersection: ({}, {})", points[1].x, points[1].y);
    let mut points2 = points;
    points2.drain(0..1);
    for destiny in points2 {
        let distance = distance_taxicab(origin, destiny);
        if distance < min_distance {
            min_distance = distance;
        }
    }
    return min_distance;
}

fn intersection(wire1: Vec<Point>, wire2: Vec<Point>) -> Vec<Point> {
    let mut inter: Vec<Point> = Vec::new();
    for point1 in wire1.clone() {
        for point2 in wire2.clone() {
            if point1.x == point2.x && point1.y == point2.y {
                inter.push(point1);
            }
        }
    }
    return inter;
}

fn main() {
    let args: Vec<String> = env::args().collect();

    // let query = &args[1];
    let filepath = &args[1];
    println!("Filepath: {}", filepath);

    let file = match fs::File::open(filepath) {
        Ok(file) => file,
        Err(_) => panic!("Unable to read from {}", filepath),
    };
    let reader = BufReader::new(file);

    let mut v: Vec<String> = Vec::new();
    for line in reader.lines() {
        v.push(line.unwrap());
    }
    println!("A: {}\nB: {}", v[0], v[1]);

    let wire_point_1: Vec<Point> = calcule_points(v[0].clone());
    let wire_point_2: Vec<Point> = calcule_points(v[1].clone());

    let inter: Vec<Point> = intersection(wire_point_1, wire_point_2);
    for i in inter.clone() {
        println!("({}, {})", i.x, i.y);
    }

    let min_distance = calcule_min_distance(inter);
    println!("Min Distance: {}", min_distance);
}
