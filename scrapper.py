import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import urllib.parse


async def scrape_linkedin(query, num_results=50):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            storage_state="linkedin_state.json",
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_query}"
        print(f"Navigating to: {url}")
        await page.goto(url)

        # Wait for the first profile card to appear
        await page.wait_for_selector('div.entity-result__content', timeout=30000)

        profiles = []
        seen_profiles = set()

        while len(profiles) < num_results:
            people = await page.query_selector_all('div.entity-result__content')
            print(f"Found {len(people)} profiles on this page so far.")

            for person in people:
                try:
                    name_el = await person.query_selector(
                        'span.entity-result__title-text > a > span[aria-hidden]'
                    )
                    name = await name_el.inner_text() if name_el else "N/A"

                    occupation_el = await person.query_selector(
                        'div.entity-result__primary-subtitle'
                    )
                    occupation = await occupation_el.inner_text() if occupation_el else "N/A"

                    location_el = await person.query_selector(
                        'div.entity-result__secondary-subtitle'
                    )
                    location = await location_el.inner_text() if location_el else "N/A"

                    unique_id = f"{name.strip()}|{occupation.strip()}|{location.strip()}"
                    if unique_id in seen_profiles:
                        continue

                    profiles.append({
                        "Name": name.strip(),
                        "Occupation": occupation.strip(),
                        "Location": location.strip()
                    })
                    seen_profiles.add(unique_id)

                    if len(profiles) >= num_results:
                        break

                except Exception as e:
                    print(f"Error parsing profile: {e}")

            if len(profiles) >= num_results:
                break

            # Try to find and click the Next button
            next_button = await page.query_selector('button[aria-label="Next"]')
            if next_button:
                print("Clicking Next button...")
                await next_button.click()
                await page.wait_for_selector('div.entity-result__content', timeout=30000)
                await page.wait_for_timeout(2000)
                continue

            # If no Next button, try scrolling
            print("No Next button found. Attempting infinite scroll...")
            previous_count = len(people)

            await page.evaluate("""() => {
                window.scrollBy(0, document.body.scrollHeight);
            }""")
            await page.wait_for_timeout(3000)

            people_after_scroll = await page.query_selector_all('div.entity-result__content')
            new_count = len(people_after_scroll)

            if new_count <= previous_count:
                print("No new results after scrolling. Exiting loop.")
                break

        await browser.close()
        return pd.DataFrame(profiles)


if __name__ == "__main__":
    query = input("Enter search keywords: ")
    how_many = int(input("How many results to scrape? "))
    df = asyncio.run(scrape_linkedin(query, num_results=how_many))
    print(df)
    df.to_csv("linkedin_profiles.csv", index=False)
    print("Data saved to linkedin_profiles.csv")
