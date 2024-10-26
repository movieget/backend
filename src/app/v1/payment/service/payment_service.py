from src.app.v1.book.entity.book import Book

async def initiate_payment(booking: Book) -> str:
    """
    TossPay 결제 URL을 생성하는 함수 (임시).
    실제 TossPay API와 통합되기 전에는 임시 URL을 반환.
    """
    # 임시로 생성된 URL을 반환하여, 실제 결제 과정 없이 리디렉션 테스트가 가능하도록 합니다.
    return f"https://mock-tosspayments.com/checkout?orderId={booking.id}&amount={booking.total_price}"
