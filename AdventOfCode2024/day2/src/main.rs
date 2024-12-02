use reqwest::blocking::Client;
use std::fs;

fn is_safe(report: &[i32]) -> bool {
    if report.windows(2).all(|pair| {
        let diff = (pair[0] - pair[1]).abs();
        (1..=3).contains(&diff)
    }) {
        report.iter().is_sorted() || report.iter().rev().is_sorted()
    } else {
        false
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cookie_content = fs::read_to_string("../cookie.txt")?.trim().to_string();

    let client = Client::new();
    let response = client
        .get("https://adventofcode.com/2024/day/2/input")
        .header("Cookie", format!("session={}", cookie_content))
        .send()?;

    let text = response.text()?;
    let lines = text.trim().split("\n");

    let reports: Vec<Vec<i32>> = lines
        .map(|line| line.split(" ").map(|x| x.parse::<i32>().unwrap()).collect())
        .collect();

    let safe = reports.iter().fold(
        0,
        |safe, report| {
            if is_safe(report) {
                safe + 1
            } else {
                safe
            }
        },
    );

    println!("Part 1: {:}", safe);

    let safe = reports.iter().fold(0, |safe, report| {
        if is_safe(report) {
            safe + 1
        } else {
            for i in 0..report.len() {
                if is_safe(
                    &report
                        .iter()
                        .take(i)
                        .chain(report.iter().skip(i + 1))
                        .cloned()
                        .collect::<Vec<i32>>(),
                ) {
                    return safe + 1;
                }
            }
            safe
        }
    });

    println!("Part 2: {:}", safe);

    Ok(())
}
