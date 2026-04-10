"""
쇼핑 리스트 앱 자동 테스트
Playwright를 사용하여 아이템 추가 / 삭제 / 체크 / 필터 / localStorage 영속성 테스트
"""

import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

HTML_PATH = Path(__file__).parent / "shopping_list.html"
FILE_URL = HTML_PATH.resolve().as_uri()

PASS = "PASS"
FAIL = "FAIL"
results = []

def log(name, status, detail=""):
    tag = f"[{status}]"
    line = f"  {tag} {name}" + (f" | {detail}" if detail else "")
    print(line)
    results.append((name, status, detail))

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        ctx = browser.new_context()
        page = ctx.new_page()

        # localStorage 초기화 후 페이지 오픈
        page.goto(FILE_URL)
        page.evaluate("localStorage.clear()")
        page.reload()

        print("\n" + "="*52)
        print(" 쇼핑 리스트 앱 자동 테스트")
        print("="*52)

        # 1. 아이템 추가
        print("\n[1] 아이템 추가")

        page.fill("#item-input", "사과")
        page.click(".btn-add")
        items = page.locator(".item-text")
        try:
            expect(items).to_have_count(1)
            expect(items.first).to_have_text("사과")
            log("아이템 1개 추가", PASS)
        except Exception as e:
            log("아이템 1개 추가", FAIL, str(e))

        page.fill("#item-input", "바나나")
        page.press("#item-input", "Enter")
        page.fill("#item-input", "오렌지")
        page.press("#item-input", "Enter")
        try:
            expect(items).to_have_count(3)
            log("Enter 키로 2개 추가 (총 3개)", PASS)
        except Exception as e:
            log("Enter 키로 2개 추가 (총 3개)", FAIL, str(e))

        page.fill("#item-input", "   ")
        page.press("#item-input", "Enter")
        try:
            expect(items).to_have_count(3)
            log("빈 입력 무시", PASS)
        except Exception as e:
            log("빈 입력 무시", FAIL, str(e))

        # 2. 통계 표시
        print("\n[2] 통계 표시")
        stats_text = page.locator("#stats").inner_text()
        try:
            assert "0 / 3 완료" == stats_text, f"실제: {stats_text!r}"
            log("통계 '0 / 3 완료' 표시", PASS)
        except AssertionError as e:
            log("통계 '0 / 3 완료' 표시", FAIL, str(e))

        # 3. 체크(완료) 기능
        print("\n[3] 체크(완료) 기능")

        checkboxes = page.locator("li input[type='checkbox']")
        checkboxes.nth(0).check()
        try:
            expect(page.locator("li.checked")).to_have_count(1)
            log("아이템 체크 -> checked 클래스 추가", PASS)
        except Exception as e:
            log("아이템 체크 -> checked 클래스 추가", FAIL, str(e))

        try:
            checked_text = page.locator("li.checked .item-text")
            td_value = checked_text.evaluate(
                "el => getComputedStyle(el).textDecoration"
            )
            assert "line-through" in td_value, f"text-decoration: {td_value!r}"
            log("완료 아이템 취소선 스타일", PASS)
        except Exception as e:
            log("완료 아이템 취소선 스타일", FAIL, str(e))

        stats_text = page.locator("#stats").inner_text()
        try:
            assert "1 / 3 완료" == stats_text, f"실제: {stats_text!r}"
            log("통계 '1 / 3 완료' 갱신", PASS)
        except AssertionError as e:
            log("통계 '1 / 3 완료' 갱신", FAIL, str(e))

        checkboxes.nth(0).uncheck()
        try:
            expect(page.locator("li.checked")).to_have_count(0)
            log("체크 해제 -> checked 클래스 제거", PASS)
        except Exception as e:
            log("체크 해제 -> checked 클래스 제거", FAIL, str(e))

        # 4. 필터 기능
        print("\n[4] 필터 기능")

        page.locator("li input[type='checkbox']").nth(0).click()
        page.wait_for_timeout(300)
        page.locator("li input[type='checkbox']").nth(1).click()
        page.wait_for_timeout(300)

        page.get_by_role("button", name="미완료", exact=True).click()
        try:
            expect(page.locator(".item-text")).to_have_count(1)
            expect(page.locator(".item-text").first).to_have_text("오렌지")
            log("미완료 필터 - 오렌지만 표시", PASS)
        except Exception as e:
            log("미완료 필터 - 오렌지만 표시", FAIL, str(e))

        page.get_by_role("button", name="완료", exact=True).click()
        page.wait_for_timeout(300)
        try:
            expect(page.locator(".item-text")).to_have_count(2)
            log("완료 필터 - 2개 표시", PASS)
        except Exception as e:
            log("완료 필터 - 2개 표시", FAIL, str(e))

        page.get_by_role("button", name="전체", exact=True).click()
        try:
            expect(page.locator(".item-text")).to_have_count(3)
            log("전체 필터 - 3개 표시", PASS)
        except Exception as e:
            log("전체 필터 - 3개 표시", FAIL, str(e))

        # 5. 아이템 삭제
        print("\n[5] 아이템 삭제")

        delete_btns = page.locator(".btn-delete")
        delete_btns.nth(2).click()
        try:
            expect(page.locator(".item-text")).to_have_count(2)
            texts = page.locator(".item-text").all_inner_texts()
            assert "오렌지" not in texts, f"오렌지가 여전히 존재: {texts}"
            log("오렌지 삭제", PASS)
        except Exception as e:
            log("오렌지 삭제", FAIL, str(e))

        # 6. 완료 항목 일괄 삭제
        print("\n[6] 완료 항목 일괄 삭제")

        page.click(".clear-btn")
        try:
            expect(page.locator(".item-text")).to_have_count(0)
            log("완료 항목 일괄 삭제 (사과·바나나 제거)", PASS)
        except Exception as e:
            log("완료 항목 일괄 삭제", FAIL, str(e))

        try:
            empty_div = page.locator("#empty")
            expect(empty_div).to_be_visible()
            log("빈 목록 안내 메시지 표시", PASS)
        except Exception as e:
            log("빈 목록 안내 메시지 표시", FAIL, str(e))

        # 7. localStorage 영속성
        print("\n[7] localStorage 영속성")

        page.fill("#item-input", "딸기")
        page.press("#item-input", "Enter")
        page.fill("#item-input", "포도")
        page.press("#item-input", "Enter")
        page.locator("li input[type='checkbox']").first.check()
        page.reload()
        try:
            expect(page.locator(".item-text")).to_have_count(2)
            expect(page.locator("li.checked")).to_have_count(1)
            log("새로고침 후 데이터·체크 상태 유지", PASS)
        except Exception as e:
            log("새로고침 후 데이터·체크 상태 유지", FAIL, str(e))

        # 결과 요약
        total = len(results)
        passed = sum(1 for _, s, _ in results if s == PASS)
        failed = total - passed

        print("\n" + "="*52)
        print(f" 결과: {passed}/{total} 통과" + (f"  ({failed}개 실패)" if failed else "  -- 전체 통과"))
        print("="*52)

        if failed:
            print("\n실패 항목:")
            for name, status, detail in results:
                if status == FAIL:
                    print(f"  * {name}: {detail}")

        time.sleep(2)
        browser.close()
        return failed == 0

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
