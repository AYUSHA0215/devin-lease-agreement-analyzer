from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import nltk
from nltk.tokenize import sent_tokenize

# Load the LEGAL-BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("nlpaueb/legal-bert-base-uncased")
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def analyze_lease(lease_text):
    """
    Analyze the lease agreement text and identify threatening clauses.

    Args:
    lease_text (str): The text of the lease agreement.

    Returns:
    list: A list of identified threatening clauses.
    """
    # Tokenize the lease text into sentences
    sentences = sent_tokenize(lease_text)

    threatening_clauses = []
    for sentence in sentences:
        results = classifier(sentence)
        for result in results:
            # Adjust the condition to match the classifier's output
            if result['label'] == 'LABEL_1' and result['score'] > 0.3:  # Adjusted threshold to 0.3
                threatening_clauses.append(sentence)

    return threatening_clauses

if __name__ == "__main__":
    # Example usage
    lease_text = """
    This lease agreement is made between the landlord and the tenant. The tenant agrees to pay a monthly rent of $1,200.
    The lease term is for one year, starting from June 1, 2023, to May 31, 2024. Early termination of the lease will result
    in a penalty fee of $2,000. The lease will automatically renew for another year unless the tenant provides a written
    notice of termination at least 60 days before the end of the lease term. I want to kill you and take all your money.
    """
    results = analyze_lease(lease_text)
    for clause in results:
        print(clause)
