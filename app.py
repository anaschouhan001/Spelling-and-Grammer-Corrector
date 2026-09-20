from flask import Flask, request, render_template
from Model import SpellCheckerModule

app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST'])
def spell():
    text = request.form.get('text', '').strip()
    if text:
        corrected_text = spell_checker_module.correct_spell(text)
        corrected_grammar_text = spell_checker_module.correct_grammar(corrected_text)
        return render_template('index.html',
                               corrected_text=corrected_text,
                               corrected_grammar_text=corrected_grammar_text)
    return render_template('index.html')

@app.route('/grammar', methods=['POST'])
def grammar():
    file = request.files.get('file')
    if file and file.filename:
        readable_file = file.read().decode('utf-8', errors='ignore').strip()
        if readable_file:
            corrected_file_text = spell_checker_module.correct_spell(readable_file)
            corrected_file_grammar_text = spell_checker_module.correct_grammar(corrected_file_text)
            return render_template('index.html',
                                   corrected_file_text=corrected_file_text,
                                   corrected_file_grammar_text=corrected_file_grammar_text)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)