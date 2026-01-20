from playwright.sync_api import sync_playwright
import random
def generate_positive_review():
    samples = [
        "The staff were incredibly friendly and made my day.",
        "Service was fast and the food was hot and fresh!",
        "Great experience overall, especially the clean dining area.",
        "Everything was perfect — from the order accuracy to the smiles.",
        "Staff were attentive, courteous, and very professional.",
        "I had a fantastic visit. Quick service and tasty food!",
        "The employees were kind and made my visit enjoyable.",
        "Wonderful atmosphere and the food was absolutely delicious!",
        "I appreciated how clean and organized the restaurant was.",
        "Excellent experience — will definitely be returning soon!"
    ]

    # Combine a few for variety, keep total words between 15 and 50
    review = ""
    while True:
        review = " ".join(random.sample(samples, k=random.randint(2, 4)))
        if 15 <= len(review.split()) <= 50:
            return review
        
def run_survey(store, date, hour, minute):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://survey.medallia.ca/?McD-GSS-FeedlessSurvey")
        page.wait_for_timeout(2000)

        try:
            page.fill('input[type="text"]', store)
            page.click('button:has-text("Begin Survey")')
            print(f"✅ Store #{store} entered and Begin clicked")
        except Exception as e:
            print("❌ Store number step failed:", e)
            return

        try:
            page.wait_for_selector("span:text('18 to 24')", timeout=10000)
            page.locator("span:text('18 to 24')").click()
            print("✅ Selected age: 18 to 24")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after age")
        except Exception as e:
            print("❌ Could not select age:", e)
            return

        try:
            page.wait_for_selector("span:text('Yes')", timeout=10000)
            page.locator("span:text('Yes')").click()
            print("✅ Selected: Yes for Rewards")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after Rewards")
        except Exception as e:
            print("❌ Failed on Rewards question:", e)
            return

        page.wait_for_timeout(2000)

        try:
            page.evaluate("""(date) => {
                const input = document.querySelector('input[type="text"]');
                input.value = date;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }""", date)
            print(f"📅 Injected and confirmed date: {date}")

            page.locator("div[role='button'][aria-label*='Hour']").nth(0).click()
            page.wait_for_selector(f'li[data-test-name*="option-{hour}-"]', timeout=5000)
            page.click(f'li[data-test-name*="option-{hour}-"]')
            print(f"🕒 Selected hour: {hour}")

            page.locator("div[role='button'][aria-label='Minutes:']").nth(0).click()
            page.wait_for_selector(f'li[data-test-name="option-{minute}"]', timeout=5000)
            page.click(f'li[data-test-name="option-{minute}"]')
            print(f"🕒 Selected minute: {minute}")

            page.fill("input[type='text']:below(:text('Amount Spent'))", "20.69")
            print("💵 Filled amount: 20.69")

            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after visit details")

        except Exception as e:
            print("❌ Failed to fill visit details:", e)
            return

        try:
            page.wait_for_selector("div:has-text('In the Restaurant at the Front Counter')", timeout=10000)
            page.click("div:has-text('In the Restaurant at the Front Counter')")
            print("✅ Selected: In the Restaurant at the Front Counter")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after order method")
        except Exception as e:
            print("❌ Failed on order method selection:", e)
            return

        try:
            page.wait_for_selector("div:has-text('Delivered at the front counter for dine in')", timeout=10000)
            page.click("div:has-text('Delivered at the front counter for dine in')")
            print("✅ Selected: Delivered at the front counter for dine in")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after delivery method")
        except Exception as e:
            print("❌ Failed on delivery method selection:", e)
            return

        try:
            page.wait_for_selector("div:has-text('McMuffins sandwich(es)')", timeout=10000)
            page.click("div:has-text('McMuffins sandwich(es)')")
            print("✅ Selected: McMuffins sandwich(es)")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after order selection")
        except Exception as e:
            print("❌ Failed on what did you order page:", e)
            return

        try:
            page.wait_for_selector("div:has-text(\"Sausage 'N Egg McMuffin®\")", timeout=10000)
            page.click("div:has-text(\"Sausage 'N Egg McMuffin®\")")
            print("✅ Selected: Sausage 'N Egg McMuffin®")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after sandwich type")
        except Exception as e:
            print("❌ Failed on sandwich type selection:", e)
            return

        try:
            page.wait_for_selector('input[value="5"]', timeout=10000)
            all_fives = page.locator('input[value="5"]')
            count = all_fives.count()
            for i in range(count):
                all_fives.nth(i).click()
            print("⭐ Selected 5 stars for all satisfaction ratings")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after satisfaction ratings")
        except Exception as e:
            print("❌ Failed on satisfaction ratings page:", e)
            return
        try:
            # Question 1: Was your order accurate? → Yes (index 0)
            page.locator("div[data-test-name='option-yes']").nth(0).click()
            print("✅ Selected: Yes for order accuracy")

            # Question 2: Did you experience a problem? → No (index 1)
            page.locator("div[data-test-name='option-no']").nth(1).click()
            print("✅ Selected: No for visit problem")

            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after order/issue questions")
        except Exception as e:
            print("❌ Failed on order accuracy/problem questions:", e)
            return

        try:
            positive_review = generate_positive_review()
            page.fill("textarea", positive_review)
            print("💬 Wrote review:", positive_review)
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after experience review")
        except Exception as e:
            print("❌ Failed on review textarea:", e)
            return
        
        try:
            page.wait_for_selector('input[value="5"][type="radio"]', timeout=5000)
            page.locator('input[value="5"][type="radio"]').first.check()
            print("✅ Selected: 5 for recommendation rating")
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after recommendation")
        except Exception as e:
            print("❌ Failed on recommendation question:", e)
            return
        
        try:
            page.wait_for_selector("button:has-text('Next')", timeout=10000)
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next on image upload page")
        except Exception as e:
            print("❌ Failed on image upload page:", e)
            return
        
        try:
            # 📮 Enter postal code in the first text input
            page.locator("input[type='text']").first.fill("A1A 1A1")
            print("📮 Entered postal code: A1A 1A1")

            # 👶 Click the second 'No' radio button (child question)
            page.locator("input[type='radio']").nth(1).click()
            print("👶 Selected: No for child under 13")

            # ➡️ Click Next
            page.click("button:has-text('Next')")
            print("➡️ Clicked: Next after postal + child")

        except Exception as e:
            print("❌ Failed on postal + child question:", e)

        try:
            # ✅ Select the radio option using data-test-name
            page.click("div[data-test-name*='option-yes,-please-email-me-my-coupon']")
            print("✅ Selected: Yes to receive coupon via email")

            # 🎯 Click Finish
            page.click("button:has-text('Finish')")
            print("🎉 Survey completed and coupon requested!")
        except Exception as e:
            print("❌ Failed on final email step:", e)

        try:
            page.wait_for_selector("input[type='text']", timeout=10000)
            page.fill("input[type='text']", "example@example.com")
            print("📧 Entered email: example@example.com")

            page.click("button:has-text('Finish')")
            print("🎉 Survey finished and email submitted!")
        except Exception as e:
            print("❌ Failed on email entry step:", e)

        page.wait_for_timeout(5000)
        browser.close()
