class Math:

    def calculate(self, expression: str) -> str:
        calc = expression.replace("x", "*").strip()

        if not calc:
            return ""

        try:
            result = eval(calc)
        except Exception:
            result = "Invalid"

        return str(result)
            
