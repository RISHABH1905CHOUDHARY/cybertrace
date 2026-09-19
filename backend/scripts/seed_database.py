"""Seed script to populate database with realistic initial data."""

import asyncio
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
import os
import random
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from app.core.security import get_password_hash
from app.database.database import AsyncSessionLocal, engine
from app.database.base import Base
from app.models.user import User, UserRole
from app.models.atm import ATM, ATMStatus
from app.models.complaint import Complaint, ComplaintStatus, FraudType
from app.models.transaction import Transaction
from app.models.location import Location, LocationType, RiskLevel


async def seed_data():
    print("Initializing tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # 1. Seed Users
        print("Seeding users...")
        users_to_create = [
            ("Cyber Admin", "admin@crimetrace.ai", "Admin@123456", UserRole.ADMIN.value),
            ("Senior Crime Analyst", "analyst@crimetrace.ai", "Analyst@123456", UserRole.ANALYST.value),
            ("Lead Investigator Sharma", "investigator@crimetrace.ai", "Invest@123456", UserRole.INVESTIGATOR.value),
            ("Nodal Officer Verma", "viewer@crimetrace.ai", "Viewer@123456", UserRole.VIEWER.value),
        ]

        for name, email, password, role in users_to_create:
            existing = await session.execute(select(User).where(User.email == email))
            if not existing.scalars().first():
                user = User(
                    name=name,
                    email=email,
                    hashed_password=get_password_hash(password),
                    role=role,
                    is_active=True,
                )
                session.add(user)
        await session.commit()

        # 2. Seed ATMs
        print("Seeding ATMs across major crime monitoring corridors...")
        existing_atms = await session.execute(select(ATM))
        if not existing_atms.scalars().first():
            atm_data = [
                # Delhi NCR Corridor
                ("ATM-SBI-DEL01", "State Bank of India", "Connaught Place Inner Circle", "B-Block, Connaught Place", "New Delhi", "New Delhi", "Delhi", 28.6315, 77.2167, ATMStatus.ACTIVE.value),
                ("ATM-HDFC-DEL02", "HDFC Bank", "Nehru Place Main Market", "Flat 101, Hemkunt Tower, Nehru Place", "New Delhi", "South Delhi", "Delhi", 28.5494, 77.2528, ATMStatus.ACTIVE.value),
                ("ATM-ICICI-DEL03", "ICICI Bank", "Lajpat Nagar Central Market", "Ring Road, Lajpat Nagar II", "New Delhi", "South East Delhi", "Delhi", 28.5680, 77.2435, ATMStatus.ACTIVE.value),
                ("ATM-AXIS-DEL04", "Axis Bank", "Karol Bagh Arya Samaj Road", "Block 15, Karol Bagh", "New Delhi", "Central Delhi", "Delhi", 28.6517, 77.1906, ATMStatus.ACTIVE.value),
                ("ATM-PNB-DEL05", "Punjab National Bank", "Chandni Chowk Red Fort Side", "Main Road, Chandni Chowk", "Delhi", "North Delhi", "Delhi", 28.6562, 77.2310, ATMStatus.ACTIVE.value),
                ("ATM-SBI-NOI01", "State Bank of India", "Sector 18 Market Noida", "Atta Market, Sector 18", "Noida", "Gautam Buddha Nagar", "Uttar Pradesh", 28.5708, 77.3260, ATMStatus.ACTIVE.value),
                ("ATM-HDFC-GGN01", "HDFC Bank", "Cyber Hub DLF Phase 2", "DLF Cyber City, Sector 24", "Gurugram", "Gurugram", "Haryana", 28.4950, 77.0895, ATMStatus.ACTIVE.value),

                # Mumbai & MMR Corridor
                ("ATM-SBI-MUM01", "State Bank of India", "Nariman Point Business Hub", "Free Press Journal Marg, Nariman Point", "Mumbai", "Mumbai City", "Maharashtra", 18.9260, 72.8235, ATMStatus.ACTIVE.value),
                ("ATM-HDFC-MUM02", "HDFC Bank", "Bandra Kurla Complex (BKC)", "G Block, BKC, Bandra East", "Mumbai", "Mumbai Suburban", "Maharashtra", 19.0657, 72.8682, ATMStatus.ACTIVE.value),
                ("ATM-ICICI-MUM03", "ICICI Bank", "Andheri East Metro Station", "MV Road, Andheri East", "Mumbai", "Mumbai Suburban", "Maharashtra", 19.1197, 72.8697, ATMStatus.ACTIVE.value),
                ("ATM-AXIS-MUM04", "Axis Bank", "Dadar West Kabutar Khana", "Ranade Road, Dadar West", "Mumbai", "Mumbai City", "Maharashtra", 19.0178, 72.8478, ATMStatus.ACTIVE.value),
                ("ATM-SBI-THN01", "State Bank of India", "Thane West Station Road", "Gokhale Road, Naupada", "Thane", "Thane", "Maharashtra", 19.1860, 72.9759, ATMStatus.ACTIVE.value),

                # Bengaluru Tech Corridor
                ("ATM-HDFC-BLR01", "HDFC Bank", "MG Road Metro Promenade", "MG Road, Shanthala Nagar", "Bengaluru", "Bengaluru Urban", "Karnataka", 12.9756, 77.6066, ATMStatus.ACTIVE.value),
                ("ATM-SBI-BLR02", "State Bank of India", "Koramangala 5th Block", "Jyoti Nivas College Road", "Bengaluru", "Bengaluru Urban", "Karnataka", 12.9352, 77.6245, ATMStatus.ACTIVE.value),
                ("ATM-ICICI-BLR03", "ICICI Bank", "Indiranagar 100ft Road", "HAL 2nd Stage, Indiranagar", "Bengaluru", "Bengaluru Urban", "Karnataka", 12.9719, 77.6412, ATMStatus.ACTIVE.value),
                ("ATM-AXIS-BLR04", "Axis Bank", "Electronic City Phase 1", "Hosur Road, Electronics City", "Bengaluru", "Bengaluru Urban", "Karnataka", 12.8452, 77.6602, ATMStatus.ACTIVE.value),

                # Hyderabad Corridor
                ("ATM-SBI-HYD01", "State Bank of India", "Hitec City Cyber Towers", "Madhapur, Hitec City", "Hyderabad", "Hyderabad", "Telangana", 17.4474, 78.3762, ATMStatus.ACTIVE.value),
                ("ATM-HDFC-HYD02", "HDFC Bank", "Banjara Hills Road No 2", "Park View Enclave, Banjara Hills", "Hyderabad", "Hyderabad", "Telangana", 17.4258, 78.4419, ATMStatus.ACTIVE.value),

                # Mewat/Nuh & Jamtara Adjacent Corridors
                ("ATM-SBI-NUH01", "State Bank of India", "Nuh Main Bazaar Branch", "Delhi-Alwar Road, Nuh", "Nuh", "Nuh", "Haryana", 28.1065, 77.0135, ATMStatus.ACTIVE.value),
                ("ATM-PNB-NUH02", "Punjab National Bank", "Tauru Sub-Division Road", "Tauru Market", "Tauru", "Nuh", "Haryana", 28.2144, 76.9535, ATMStatus.ACTIVE.value),
                ("ATM-SBI-JAM01", "State Bank of India", "Jamtara Court Road Branch", "Main Court Road", "Jamtara", "Jamtara", "Jharkhand", 23.9628, 86.8016, ATMStatus.ACTIVE.value),
            ]

            created_atms = []
            for code, bank, branch, addr, city, dist, state, lat, lon, st in atm_data:
                atm = ATM(
                    atm_id=code,
                    bank_name=bank,
                    branch_name=branch,
                    address=addr,
                    city=city,
                    district=dist,
                    state=state,
                    latitude=lat,
                    longitude=lon,
                    status=st,
                )
                session.add(atm)
                created_atms.append(atm)
            await session.commit()
            print(f"Seeded {len(created_atms)} ATMs.")

        # 3. Seed Complaints
        print("Seeding cybercrime complaints...")
        existing_comp = await session.execute(select(Complaint))
        if not existing_comp.scalars().first():
            complaint_types = [
                (FraudType.UPI_FRAUD.value, 48000.0, "Victim scammed via fake electricity bill payment link and malicious APK.", "New Delhi", "South Delhi", "Delhi", "Kalkaji", 28.5401, 77.2580),
                (FraudType.ATM_FRAUD.value, 60000.0, "Card cloned at shopping mall; unauthorized ATM withdrawals followed.", "New Delhi", "Central Delhi", "Delhi", "Connaught Place", 28.6328, 77.2195),
                (FraudType.PHISHING.value, 125000.0, "Fake KYC upgrade call spoofing bank official; net banking compromised.", "Noida", "Gautam Buddha Nagar", "Uttar Pradesh", "Sector 18", 28.5715, 77.3245),
                (FraudType.BANKING_FRAUD.value, 240000.0, "Unauthorized RTGS/IMPS transfer triggered via compromised credentials.", "Gurugram", "Gurugram", "Haryana", "DLF Phase 2", 28.4960, 77.0880),
                (FraudType.ONLINE_SHOPPING_FRAUD.value, 35000.0, "Deceptive social media store advertising discounted electronics.", "New Delhi", "North Delhi", "Delhi", "Civil Lines", 28.6814, 77.2228),
                (FraudType.CARD_FRAUD.value, 82000.0, "Credit card skimmed; multiple cash withdrawals at unattended ATMs.", "Mumbai", "Mumbai Suburban", "Maharashtra", "Bandra East", 19.0645, 72.8660),
                (FraudType.UPI_FRAUD.value, 95000.0, "Fake lottery QR code scan lured victim into entering UPI PIN.", "Mumbai", "Mumbai City", "Maharashtra", "Nariman Point", 18.9280, 72.8250),
                (FraudType.ATM_FRAUD.value, 40000.0, "Shoulder surfing and card swap at ATM booth.", "Bengaluru", "Bengaluru Urban", "Karnataka", "Koramangala", 12.9340, 77.6250),
                (FraudType.PHISHING.value, 180000.0, "Investment scam via Telegram groups promising daily stock returns.", "Bengaluru", "Bengaluru Urban", "Karnataka", "Indiranagar", 12.9730, 77.6400),
                (FraudType.UPI_FRAUD.value, 75000.0, "OLX army officer scam deception during furniture purchase.", "Hyderabad", "Hyderabad", "Telangana", "Madhapur", 17.4490, 78.3750),
                (FraudType.BANKING_FRAUD.value, 320000.0, "Sextortion and extortion scam coerced payments to multiple mules.", "Nuh", "Nuh", "Haryana", "Tauru Road", 28.1100, 77.0120),
                (FraudType.OTHER.value, 50000.0, "Remote access app scam (AnyDesk/TeamViewer) under guise of tech support.", "Jamtara", "Jamtara", "Jharkhand", "Station Area", 23.9610, 86.8030),
            ]

            now = datetime.now(timezone.utc)
            created_complaints = []
            for idx, (f_type, amt, desc, city, dist, state, area, lat, lon) in enumerate(complaint_types, 1):
                c_date = now - timedelta(days=random.randint(1, 60), hours=random.randint(1, 12))
                t_date = c_date - timedelta(hours=random.randint(2, 24))
                status_choice = random.choice([
                    ComplaintStatus.REPORTED.value,
                    ComplaintStatus.UNDER_INVESTIGATION.value,
                    ComplaintStatus.RESOLVED.value,
                ])
                comp = Complaint(
                    complaint_id=f"CR-2026-NCRP{idx:04d}",
                    complaint_type="Cyber Fraud",
                    fraud_type=f_type,
                    amount=amt,
                    complaint_date=c_date,
                    transaction_date=t_date,
                    state=state,
                    district=dist,
                    city=city,
                    area=area,
                    latitude=lat,
                    longitude=lon,
                    status=status_choice,
                    description=desc,
                    source="National Cyber Crime Reporting Portal",
                )
                session.add(comp)
                created_complaints.append(comp)

            await session.commit()
            print(f"Seeded {len(created_complaints)} complaints.")

        # 4. Seed Transactions
        print("Seeding transactions and withdrawal records...")
        existing_txns = await session.execute(select(Transaction))
        if not existing_txns.scalars().first():
            atms = (await session.execute(select(ATM))).scalars().all()
            complaints = (await session.execute(select(Complaint))).scalars().all()

            txns = []
            for i in range(1, 40):
                atm = random.choice(atms)
                is_fraud = random.choice([True, False, False])
                linked_comp = random.choice(complaints) if is_fraud and complaints else None
                txn_amount = random.choice([5000.0, 10000.0, 15000.0, 20000.0, 40000.0, 50000.0])
                
                txn_date = date.today() - timedelta(days=random.randint(0, 30))
                txn_time = time(random.randint(6, 23), random.randint(0, 59), random.randint(0, 59))

                txn = Transaction(
                    transaction_id=f"TXN-2026-{10000 + i}",
                    atm_id=atm.id,
                    atm_code=atm.atm_id,
                    transaction_date=txn_date,
                    transaction_time=txn_time,
                    amount=txn_amount,
                    transaction_type="cash_withdrawal",
                    city=atm.city,
                    district=atm.district,
                    latitude=atm.latitude,
                    longitude=atm.longitude,
                    is_fraud=is_fraud,
                    complaint_id=linked_comp.id if linked_comp else None,
                )
                session.add(txn)
                txns.append(txn)

            await session.commit()
            print(f"Seeded {len(txns)} transactions.")

        # 5. Seed Locations / POIs
        print("Seeding geographic locations and hotspot regions...")
        existing_locs = await session.execute(select(Location))
        if not existing_locs.scalars().first():
            locs = [
                ("Special Cell Cyber Crime Police Station (IFSO)", LocationType.POLICE_STATION.value, "South West Delhi", "Delhi", 28.5823, 77.1654, 3000, RiskLevel.LOW.value),
                ("Noida Cyber Crime Police Station Sector 36", LocationType.POLICE_STATION.value, "Gautam Buddha Nagar", "Uttar Pradesh", 28.5772, 77.3468, 2500, RiskLevel.LOW.value),
                ("Mewat Cash-out Corridors (Tauru-Nuh)", LocationType.HOTSPOT.value, "Nuh", "Haryana", 28.1150, 77.0100, 10000, RiskLevel.CRITICAL.value),
                ("Jamtara Cyber Syndicate Hub", LocationType.HOTSPOT.value, "Jamtara", "Jharkhand", 23.9620, 86.8020, 8000, RiskLevel.CRITICAL.value),
                ("Nehru Place Commercial High-Traffic Zone", LocationType.HOTSPOT.value, "South Delhi", "Delhi", 28.5490, 77.2530, 2000, RiskLevel.HIGH.value),
                ("BKC Financial Center Cluster", LocationType.HOTSPOT.value, "Mumbai Suburban", "Maharashtra", 19.0660, 72.8670, 2500, RiskLevel.MEDIUM.value),
            ]
            for name, l_type, dist, state, lat, lon, rad, risk in locs:
                loc = Location(
                    name=name,
                    location_type=l_type,
                    district=dist,
                    state=state,
                    latitude=lat,
                    longitude=lon,
                    radius_meters=rad,
                    risk_level=risk,
                )
                session.add(loc)
            await session.commit()
            print("Seeded geographic points.")

    print("\nDatabase seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())
