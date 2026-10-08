import streamlit as st
from datetime import datetime
import io

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Trà Sữa - Tính Tiền",
    page_icon="🧋",
    layout="centered"
)

# ==============================
# DỮ LIỆU MENU
# ==============================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa thái xanh": 32000,
    "Trà sữa thái đỏ": 32000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
}

SIZE_PRICE = {
    "S": 0,
    "M": 5000,
    "L": 10000
}

TOPPING_PRICE = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Nha đam": 5000,
}

SUGAR_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]

ICE_LEVELS = [
    "100%",
    "70%",
    "50%",
    "30%",
    "0%"
]

# ==============================
# KHỞI TẠO SESSION
# ==============================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# ==============================
# TIÊU ĐỀ
# ==============================

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("💵 Hệ thống tính tiền hóa đơn")

st.divider()

# ==============================
# THÔNG TIN KHÁCH HÀNG
# ==============================

st.header("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

st.divider()

# ==============================
# CHỌN MÓN
# ==============================

st.header("🧋 Thêm món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / nước",
        list(MENU.keys())
    )

    size = st.selectbox(
        "Size",
        list(SIZE_PRICE.keys())
    )

    topping = st.selectbox(
        "Topping",
        list(TOPPING_PRICE.keys())
    )

with col2:
    sugar = st.selectbox(
        "Mức độ đường",
        SUGAR_LEVELS,
        index=0
    )

    ice = st.selectbox(
        "Mức độ đá",
        ICE_LEVELS,
        index=0
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

# ==============================
# TÍNH GIÁ MÓN
# ==============================

base_price = MENU[drink]
size_price = SIZE_PRICE[size]
topping_price = TOPPING_PRICE[topping]

unit_price = base_price + size_price + topping_price
total_price = unit_price * quantity

st.info(
    f"💰 Đơn giá: **{unit_price:,} VNĐ** | "
    f"Thành tiền: **{total_price:,} VNĐ**"
)

# ==============================
# THÊM MÓN
# ==============================

if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):

    item = {
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "ice": ice,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_price": total_price
    }

    st.session_state.cart.append(item)

    st.success(f"Đã thêm {quantity} x {drink} vào hóa đơn!")

# ==============================
# HIỂN THỊ GIỎ HÀNG
# ==============================

st.divider()
st.header("🛒 Danh sách món")

if len(st.session_state.cart) == 0:

    st.warning("Chưa có món nào trong hóa đơn.")

else:

    grand_total = 0

    for i, item in enumerate(st.session_state.cart):

        grand_total += item["total_price"]

        with st.container(border=True):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.markdown(
                    f"### 🧋 {item['drink']}"
                )

                st.write(
                    f"Size: **{item['size']}** | "
                    f"Topping: **{item['topping']}**"
                )

                st.write(
                    f"Đường: **{item['sugar']}** | "
                    f"Đá: **{item['ice']}**"
                )

            with col2:
                st.write(
                    f"Số lượng: **{item['quantity']}**"
                )

                st.write(
                    f"Đơn giá: **{item['unit_price']:,} VNĐ**"
                )

                st.write(
                    f"**{item['total_price']:,} VNĐ**"
                )

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{i}"
                ):
                    st.session_state.cart.pop(i)
                    st.rerun()

    st.divider()

    st.markdown(
        f"""
        <div style="
            background-color:#f5f5f5;
            padding:20px;
            border-radius:15px;
            text-align:right;
        ">
            <h2>TỔNG TIỀN</h2>
            <h1 style="color:#e63946;">
                {grand_total:,} VNĐ
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================
# THANH TOÁN
# ==============================

st.divider()
st.header("💳 Thanh toán")

if len(st.session_state.cart) > 0:

    payment_method = st.radio(
        "Phương thức thanh toán",
        ["💵 Tiền mặt", "🏦 Chuyển khoản"],
        horizontal=True
    )

    if st.button(
        "💰 THANH TOÁN",
        type="primary",
        use_container_width=True
    ):

        if customer_name.strip() == "":
            st.error("⚠️ Vui lòng nhập tên khách hàng!")
        else:

            grand_total = sum(
                item["total_price"]
                for item in st.session_state.cart
            )

            invoice_number = datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )

            invoice = {
                "invoice_number": invoice_number,
                "customer": customer_name,
                "items": st.session_state.cart.copy(),
                "total": grand_total,
                "payment": payment_method,
                "time": datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
            }

            st.session_state.invoice = invoice

            st.success("🎉 Thanh toán thành công!")

# ==============================
# HIỂN THỊ HÓA ĐƠN
# ==============================

if st.session_state.invoice is not None:

    invoice = st.session_state.invoice

    st.divider()
    st.header("🧾 HÓA ĐƠN")

    # Nội dung hóa đơn hiển thị
    st.markdown(
        f"""
        <div style="
            border:2px solid #333;
            border-radius:15px;
            padding:25px;
            background:white;
        ">

        <h1 style="text-align:center;">
            🧋 QUÁN TRÀ SỮA
        </h1>

        <p style="text-align:center;">
            HÓA ĐƠN THANH TOÁN
        </p>

        <hr>

        <p>
        <b>Mã hóa đơn:</b> {invoice['invoice_number']}<br>
        <b>Khách hàng:</b> {invoice['customer']}<br>
        <b>Thời gian:</b> {invoice['time']}<br>
        <b>Thanh toán:</b> {invoice['payment']}
        </p>

        <hr>
        """,
        unsafe_allow_html=True
    )

    for index, item in enumerate(invoice["items"], start=1):

        st.markdown(
            f"""
            <div style="
                padding:10px 0;
                border-bottom:1px solid #ddd;
            ">

            <b>{index}. {item['drink']}</b><br>

            Size: {item['size']} |
            Topping: {item['topping']}<br>

            Đường: {item['sugar']} |
            Đá: {item['ice']}<br>

            SL: {item['quantity']} ×
            {item['unit_price']:,} VNĐ

            <br>

            <b>Thành tiền:
            {item['total_price']:,} VNĐ</b>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <hr>

        <h2 style="text-align:right;">
        TỔNG CỘNG:
        {invoice['total']:,} VNĐ
        </h2>

        <p style="text-align:center;">
        Cảm ơn quý khách! ❤️<br>
        Hẹn gặp lại!
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ==============================
    # TẠO FILE HÓA ĐƠN
    # ==============================

    invoice_text = ""

    invoice_text += "====================================\n"
    invoice_text += "           QUÁN TRÀ SỮA\n"
    invoice_text += "          HÓA ĐƠN THANH TOÁN\n"
    invoice_text += "====================================\n"

    invoice_text += f"Mã hóa đơn: {invoice['invoice_number']}\n"
    invoice_text += f"Khách hàng: {invoice['customer']}\n"
    invoice_text += f"Thời gian: {invoice['time']}\n"
    invoice_text += f"Thanh toán: {invoice['payment']}\n"

    invoice_text += "------------------------------------\n"

    for index, item in enumerate(invoice["items"], start=1):

        invoice_text += (
            f"{index}. {item['drink']}\n"
            f"   Size: {item['size']}\n"
            f"   Topping: {item['topping']}\n"
            f"   Đường: {item['sugar']}\n"
            f"   Đá: {item['ice']}\n"
            f"   Số lượng: {item['quantity']}\n"
            f"   Đơn giá: {item['unit_price']:,} VNĐ\n"
            f"   Thành tiền: {item['total_price']:,} VNĐ\n"
        )

        invoice_text += "------------------------------------\n"

    invoice_text += (
        f"TỔNG CỘNG: {invoice['total']:,} VNĐ\n"
    )

    invoice_text += "====================================\n"
    invoice_text += "       Cảm ơn quý khách!\n"
    invoice_text += "====================================\n"

    # ==============================
    # NÚT XUẤT HÓA ĐƠN
    # ==============================

    st.download_button(
        label="📥 Xuất hóa đơn",
        data=invoice_text.encode("utf-8"),
        file_name=f"hoa_don_{invoice['invoice_number']}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # ==============================
    # TẠO HÓA ĐƠN MỚI
    # ==============================

    if st.button(
        "🆕 Tạo hóa đơn mới",
        use_container_width=True
    ):

        st.session_state.cart = []
        st.session_state.invoice = None
        st.session_state.customer_name = ""

        st.rerun()
