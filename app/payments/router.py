import uuid
import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models import User, Payment
from app.groups.service import get_group, active_members_on
from app.expenses.service import get_exchange_rate

router = APIRouter(tags=["payments"])
templates = Jinja2Templates(directory="templates")


def flash(response: RedirectResponse, message: str, category: str = "success") -> None:
    response.set_cookie("flash_message", message, max_age=10, httponly=True)
    response.set_cookie("flash_category", category, max_age=10, httponly=True)


async def record_payment(
    db: AsyncSession,
    group_id: uuid.UUID,
    from_user_id: uuid.UUID,
    to_user_id: uuid.UUID,
    amount: Decimal,
    currency_code: str,
    date: datetime.date,
    notes: str = None,
    source_row: int = None,
) -> Payment:
    rate = await get_exchange_rate(db, currency_code, date)
    amount_inr = (amount * rate).quantize(Decimal("0.01"))

    payment = Payment(
        group_id=group_id,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        amount=amount,
        currency_code=currency_code,
        amount_inr=amount_inr,
        date=date,
        notes=notes,
        source_row=source_row,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


@router.get("/groups/{group_id}/payments/new", response_class=HTMLResponse)
async def new_payment_page(
    group_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = await get_group(db, group_id)
    if not group:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
    members = await active_members_on(db, group_id, datetime.date.today())
    return templates.TemplateResponse(
        "payments/create.html",
        {
            "request": request,
            "current_user": current_user,
            "group": group,
            "members": members,
            "today": datetime.date.today().isoformat(),
        },
    )


@router.post("/groups/{group_id}/payments")
async def create_payment(
    group_id: uuid.UUID,
    request: Request,
    from_user_id: uuid.UUID = Form(...),
    to_user_id: uuid.UUID = Form(...),
    amount: str = Form(...),
    currency_code: str = Form(default="INR"),
    date: str = Form(...),
    notes: str = Form(default=""),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = await get_group(db, group_id)
    if not group:
        resp = RedirectResponse(url="/", status_code=303)
        flash(resp, "Group not found.", "error")
        return resp

    try:
        payment_amount = Decimal(amount.replace(",", ""))
        payment_date = datetime.date.fromisoformat(date)
    except ValueError as e:
        resp = RedirectResponse(url=f"/groups/{group_id}/payments/new", status_code=303)
        flash(resp, f"Invalid input: {e}", "error")
        return resp

    try:
        await record_payment(
            db=db,
            group_id=group_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=payment_amount,
            currency_code=currency_code.upper(),
            date=payment_date,
            notes=notes or None,
        )
    except ValueError as e:
        resp = RedirectResponse(url=f"/groups/{group_id}/payments/new", status_code=303)
        flash(resp, str(e), "error")
        return resp

    resp = RedirectResponse(url=f"/groups/{group_id}/balances", status_code=303)
    flash(resp, "Payment recorded successfully.")
    return resp
