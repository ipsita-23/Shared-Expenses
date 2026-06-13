import asyncio
import datetime
from decimal import Decimal

from sqlalchemy import select
from app.database import SessionLocal, Base, engine
from app.models import Currency, ExchangeRate, User, Group, GroupMember
from app.auth.service import hash_password

async def seed_data():
    async with SessionLocal() as db:
        # 1. Add Currencies
        inr = await db.get(Currency, "INR")
        if not inr:
            inr = Currency(code="INR", name="Indian Rupee")
            db.add(inr)
        
        usd = await db.get(Currency, "USD")
        if not usd:
            usd = Currency(code="USD", name="US Dollar")
            db.add(usd)
        
        await db.flush()

        # 2. Add Exchange Rates for USD to INR from 2026-02-01 to 2026-04-30
        start_date = datetime.date(2026, 2, 1)
        end_date = datetime.date(2026, 4, 30)
        curr_date = start_date
        
        # We can seed a slightly varying rate around 83.50
        base_rate = Decimal("83.50")
        rate_count = 0
        
        while curr_date <= end_date:
            # Check if rate already exists
            stmt = select(ExchangeRate).where(
                ExchangeRate.currency_code == "USD",
                ExchangeRate.rate_date == curr_date
            )
            res = await db.execute(stmt)
            existing_rate = res.scalar_one_or_none()
            
            if not existing_rate:
                # Slight variation based on date day to make it interesting
                variation = Decimal(str((curr_date.day % 10 - 5) * 0.05))
                rate_val = base_rate + variation
                rate = ExchangeRate(
                    currency_code="USD",
                    rate_date=curr_date,
                    rate_to_inr=rate_val
                )
                db.add(rate)
                rate_count += 1
            
            curr_date += datetime.timedelta(days=1)
        
        print(f"Seeded {rate_count} exchange rate entries.")

        # 3. Create Admin User (Ipsita)
        stmt = select(User).where(User.email == "ipsita@example.com")
        res = await db.execute(stmt)
        ipsita = res.scalar_one_or_none()
        if not ipsita:
            ipsita = User(
                name="Ipsita",
                email="ipsita@example.com",
                hashed_password=hash_password("password123")
            )
            db.add(ipsita)
            await db.flush()
            print("Seeded User: Ipsita (ipsita@example.com)")
        else:
            print("User Ipsita already exists.")

        # Seed additional users for demo
        stmt = select(User).where(User.email == "rohan@example.com")
        res = await db.execute(stmt)
        rohan = res.scalar_one_or_none()
        if not rohan:
            rohan = User(
                name="Rohan",
                email="rohan@example.com",
                hashed_password=hash_password("password123")
            )
            db.add(rohan)
            await db.flush()
            print("Seeded User: Rohan (rohan@example.com)")

        stmt = select(User).where(User.email == "aisha@example.com")
        res = await db.execute(stmt)
        aisha = res.scalar_one_or_none()
        if not aisha:
            aisha = User(
                name="Aisha",
                email="aisha@example.com",
                hashed_password=hash_password("password123")
            )
            db.add(aisha)
            await db.flush()
            print("Seeded User: Aisha (aisha@example.com)")

        # 4. Create "Flat Expenses" Group
        stmt = select(Group).where(Group.name == "Flat Expenses")
        res = await db.execute(stmt)
        group = res.scalar_one_or_none()
        if not group:
            group = Group(name="Flat Expenses")
            db.add(group)
            await db.flush()
            print("Created Group: Flat Expenses")
        
        # Add members to group starting from 2026-02-01
        for user in [ipsita, rohan, aisha]:
            stmt = select(GroupMember).where(
                GroupMember.group_id == group.id,
                GroupMember.user_id == user.id
            )
            res = await db.execute(stmt)
            member = res.scalar_one_or_none()
            if not member:
                member = GroupMember(
                    group_id=group.id,
                    user_id=user.id,
                    joined_at=datetime.date(2026, 2, 1)
                )
                db.add(member)
                print(f"Added {user.name} to Flat Expenses group starting 2026-02-01.")

        await db.commit()
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
