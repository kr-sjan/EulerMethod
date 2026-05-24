from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    inputs = None
    final_y = None

    if request.method == 'POST':
        # 1. Kuhaon ang data gikan sa HTML form
        equation_input = request.form.get('equation', '').strip()
        x0 = float(request.form.get('x0', 0))
        y0 = float(request.form.get('y0', 0))
        h = float(request.form.get('h', 0.1))
        xn = float(request.form.get('xn', 0))

        # Tipigan ang orihinal nga gi-type sa user para i-display sa Answer box
        orihinal_nga_equation = equation_input

        # === KANI ANG "BACKSTAGE TRANSLATOR" PARA SA TRIGO UG E ===
        # Usbon ang ^ ngadto sa ** para sa exponent
        equation_input = equation_input.replace('^', '**')
        
        # I-auto-replace ang 'e^' o 'e**' para mailhan nga math.exp
        # (Gi-handle pod niini kung nag-type silag e^x o e^(x))
        equation_input = equation_input.replace('e**x', 'math.exp(x)')
        equation_input = equation_input.replace('e^x', 'math.exp(x)')
        
        # I-auto-replace ang mga trigo ug log para butangan og 'math.' sa unahan automatic
        equation_input = equation_input.replace('sin', 'math.sin')
        equation_input = equation_input.replace('cos', 'math.cos')
        equation_input = equation_input.replace('tan', 'math.tan')
        equation_input = equation_input.replace('log', 'math.log')

        # 2. EULER'S METHOD LOOP
        results = []
        current_x = x0
        current_y = y0
        step = 0

        # I-save ang sugod nga point (Step 0)
        results.append({
            'step': step,
            'x': round(current_x, 4),
            'y': round(current_y, 4)
        })

        try:
            # Mag-loop hangtod maabot ang target value xn
            while current_x < xn:
                # I-assign ang x ug y para magamit sa eval()
                x = current_x
                y = current_y

                # I-evaluate ang nindot nga equation
                slope = eval(equation_input)

                # Euler's Formula: y_next = y + h * slope
                current_y = current_y + (h * slope)
                current_x = current_x + h
                step += 1

                results.append({
                    'step': step,
                    'x': round(current_x, 4),
                    'y': round(current_y, 4)
                })

            final_y = round(current_y, 4)

        except Exception as e:
            # Kung naay error sa pag-compute (sama sa sayop nga sinulat)
            orihinal_nga_equation = f"Error sa pag-compute! Palihug i-check ang pagka-sulat. ({str(e)})"
            results = []
            final_y = "Error"

        # Tipigan ang mga inputs para ibalik sa HTML
        inputs = {
            'eq_text': orihinal_nga_equation,
            'x0': x0,
            'y0': y0,
            'h': h,
            'xn': xn
        }

    return render_template('index.html', results=results, inputs=inputs, final_y=final_y)

if __name__ == '__main__':
    app.run(debug=True)