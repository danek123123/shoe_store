-- SQL для PostgreSQL (не выполняется в SQLite)

CREATE OR REPLACE FUNCTION calc_total_pg(price NUMERIC, quantity INTEGER)
RETURNS NUMERIC AS $$
BEGIN
    IF quantity <= 0 THEN
        RETURN 0;
    END IF;
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE create_order_pg(
    p_user_id INTEGER,
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order_id INTEGER;
    v_price NUMERIC;
    v_available INTEGER;
BEGIN
    SELECT quantity_available, price INTO v_available, v_price
    FROM stock_items si
    JOIN products p ON p.product_id = si.product_id
    WHERE si.stock_item_id = p_stock_item_id;

    IF v_available IS NULL OR v_available < p_qty THEN
        RAISE EXCEPTION 'Недостаточно товара на складе';
    END IF;

    INSERT INTO orders (order_date, user_id)
    VALUES (CURRENT_TIMESTAMP, p_user_id)
    RETURNING order_id INTO v_order_id;

    INSERT INTO order_items (order_id, stock_item_id, quantity, price)
    VALUES (v_order_id, p_stock_item_id, p_qty, v_price);

    UPDATE stock_items
    SET quantity_available = quantity_available - p_qty
    WHERE stock_item_id = p_stock_item_id;
END;
$$;


CREATE OR REPLACE PROCEDURE write_off_stock_pg(
    p_stock_item_id INTEGER,
    p_qty INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_available INTEGER;
BEGIN
    SELECT quantity_available INTO v_available
    FROM stock_items WHERE stock_item_id = p_stock_item_id;

    IF v_available IS NULL OR v_available < p_qty THEN
        RAISE NOTICE 'Недостаточно товара на складе!';
        RETURN;
    END IF;

    UPDATE stock_items
    SET quantity_available = quantity_available - p_qty
    WHERE stock_item_id = p_stock_item_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Ошибка при списании: %', SQLERRM;
END;
$$;
