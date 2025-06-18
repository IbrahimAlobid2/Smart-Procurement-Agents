from flask import Flask, render_template, request, send_file, redirect, flash
from crew import procurement_crew
from src.utils import clean_report
import time
import os

OUTPUT_FOLDER = 'src/ai-agent-output'
DEFAULT_WEBSITES = [
    'sy.opensooq.com',
    'sukar.com',
    'syriamarket.net'
]

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Create the output folder if it does not already exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Clean the output folder at startup
for filename in os.listdir(OUTPUT_FOLDER):
    path = os.path.join(OUTPUT_FOLDER, filename)
    try:
        os.remove(path)
    except Exception:
        print("Failed to remove file:", path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        top_recommendations_no = request.form.get('top_recommendations_no')
        language = request.form.get('language')

        # Validate all form fields (robustness)
        if not product_name or not top_recommendations_no or not language:
            flash("All fields are required.")
            return redirect(request.url)
        
        try:
            output_dir = OUTPUT_FOLDER
            os.makedirs(output_dir, exist_ok=True)

            # Prepare input variables for the Crew workflow
            inputs = {
                'product_name': product_name,
                'no_keywords': 3,
                'websites_list': DEFAULT_WEBSITES,
                'language': language,
                'score_th': 0.5,
                'top_recommendations_no': int(top_recommendations_no),
                'country_name': 'Syria',
                'search_results': os.path.join(output_dir, 'step_2_search_results.json'),
                'products_file': os.path.join(output_dir, 'step_3_products_file.json')
            }

            # Start the workflow (launch the agents)
            procurement_crew.kickoff(inputs=inputs)
            print("Procurement crew kickoff completed")

            # Wait dynamically until the report is generated (simple polling)
            result_html = os.path.join(output_dir, 'step_4_procurement_report.html')
            for _ in range(30):
                if os.path.exists(result_html):
                    break
                time.sleep(1.0)

            if os.path.exists(result_html):
                clean_report(result_html)
                return render_template('result.html', website_file='step_4_procurement_report.html')
            else:
                flash('Error: Report not generated. Please try again.')
                return redirect(request.url)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(request.url)

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    flash("File not found.")
    return redirect('/')

@app.route('/preview/<filename>')
def preview_file(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        flash("File not found.")
        return redirect('/')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

if __name__ == '__main__':
    app.run(debug=True)
