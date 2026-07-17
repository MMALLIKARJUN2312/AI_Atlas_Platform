from app.core.event_loop import configure_event_loop

configure_event_loop()

import asyncio

import asyncio
from time import perf_counter

from app.database.session import AsyncSessionLocal
from app.services.dataset_import_service import DatasetImportService

async def main() -> None:
    start = perf_counter()

    async with AsyncSessionLocal() as session:
        service = DatasetImportService(session)

        import_summary = await service.import_all()

    elapsed = perf_counter() - start

    print("\n" + "=" * 50)
    print(" AI Atlas Dataset Import Summary")
    print("=" * 50)
    print(f" Companies Imported : {import_summary['companies']}")
    print(f" Problems Imported  : {import_summary['problems']}")
    print(f" Mappings Imported  : {import_summary['mappings']}")
    print(f" Sectors Imported   : {import_summary['sectors']}")
    print("=" * 50)
    print(f" Import Completed Successfully in {elapsed:.2f} seconds")
    print("=" * 50)
    
if __name__ == "__main__":
    asyncio.run(main())