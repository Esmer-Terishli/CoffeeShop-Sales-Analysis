import csv
from textblob import TextBlob

def classify_by_text(content):
    """
    Classifies sentiment based solely on text content.
    """
    try:
        analysis = TextBlob(content)
        if analysis.sentiment.polarity > 0.1:
            return "positive"
        elif analysis.sentiment.polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "neutral"

def add_sentiment_to_existing_csv(input_file):
    """
    Reads the original CSV file, adds sentiment analysis based on text content,
    and overwrites the original file with the new data.
    """
    
    rows = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['ReviewType']
        
        for row in reader:
            row['ReviewType'] = classify_by_text(row['content'])
            rows.append(row)
    
    with open(input_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    input_csv = "reviews_scraping_tripadvisor.csv" 
    
    print("Performing text-based sentiment analysis...")
    add_sentiment_to_existing_csv(input_csv)
    print(f"Done! File '{input_csv}' has been updated (ReviewType added based on text content).")