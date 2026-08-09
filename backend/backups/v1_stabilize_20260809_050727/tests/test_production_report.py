from app.health.production_report import ProductionReport

report = ProductionReport().generate()

print("PRODUCTION REPORT:")
print(report)
