from pathlib import Path
from src.db_init import get_connection

def main():
    q_file = Path('queries/04_check_queries.sql')
    text = q_file.read_text(encoding='utf-8')
    
    # Простой парсинг запросов по ';'
    queries = [q.strip() for q in text.split(';') if q.strip()]
    
    with open('docs/04_query_results.md', 'w', encoding='utf-8') as f:
        f.write("# Результаты SQL-запросов\n\n")
        with get_connection() as conn:
            for i, q in enumerate(queries, 1):
                # Извлекаем комментарий перед запросом
                lines = q.split('\n')
                title = lines[0].replace('--', '').strip() if lines[0].startswith('--') else f"Запрос {i}"
                sql = '\n'.join(lines[1:]).strip() if lines[0].startswith('--') else q
                
                f.write(f"## {title}\n\n```sql\n{sql}\n```\n\n")
                try:
                    cursor = conn.execute(sql)
                    rows = cursor.fetchall()
                    if rows:
                        # Заголовки
                        cols = [desc[0] for desc in cursor.description]
                        f.write("| " + " | ".join(cols) + " |\n")
                        f.write("|" + "---|" * len(cols) + "\n")
                        for row in rows:
                            f.write("| " + " | ".join(str(v) for v in tuple(row)) + " |\n")
                    else:
                        f.write("*Нет данных*\n")
                except Exception as e:
                    f.write(f"*Ошибка: {e}*\n")
                f.write("\n---\n\n")
    print("OK: docs/04_query_results.md создан")

if __name__ == "__main__":
    main()
