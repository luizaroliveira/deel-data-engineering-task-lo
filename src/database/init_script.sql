-- These statements create an extra schema and databases 
-- that will be needed during this exercise, 
-- together with some initial data for testing.
DROP TABLE IF EXISTS analytical_platform.report_operations_arguments;
DROP TABLE IF EXISTS analytical_platform.report_operations;
DROP SCHEMA IF EXISTS analytical_platform;
CREATE SCHEMA IF NOT EXISTS analytical_platform;
CREATE TABLE IF NOT EXISTS analytical_platform.report_operations (
    report_id SERIAL PRIMARY KEY,
    report_description VARCHAR(100) NOT NULL,
    report_long_description varchar(500) NOT NULL,
    argument_usage varchar(500) NULL,
    enabled bool NOT NULL DEFAULT true,
    query varchar(5000) NOT NULL,
    updated_at timestamp(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
    UNIQUE (report_description)
);
CREATE TABLE IF NOT EXISTS analytical_platform.report_operations_arguments (
    argument_id SERIAL PRIMARY KEY,
    report_id serial REFERENCES analytical_platform.report_operations(report_id),
    argument_name VARCHAR(50) NOT NULL,
    argument_position smallint not null,
    associated_field VARCHAR(200) NULL,
    argument_description VARCHAR(500) NOT NULL,
    default_value VARCHAR(200) NULL,
    embedded bool not null default false,
    optional bool NOT NULL DEFAULT false,
    block VARCHAR(20) null,
    example varchar(256) NOT NULL,
    updated_at timestamp(3) NULL DEFAULT CURRENT_TIMESTAMP(3),
    UNIQUE (report_id, argument_name),
    UNIQUE (report_id, argument_position)
);
INSERT INTO analytical_platform.report_operations (
        report_id,
        report_description,
        report_long_description,
        enabled,
        query,
        updated_at
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_report_id_seq'::regclass
        ),
        'Open orders by delivery date and status',
        'Returns the amount of orders where the status is not "completed", grouped by delivery_date and status. Ordered by delivery date desc.',
        true,
        'SELECT	count(1) as amount,	delivery_date, status FROM operations.orders where status != ''COMPLETED'' group by 2,3 order by amount desc',
        CURRENT_TIMESTAMP(3)
    );
INSERT INTO analytical_platform.report_operations (
        report_id,
        report_description,
        report_long_description,
        enabled,
        query,
        updated_at
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_report_id_seq'::regclass
        ),
        'Top 3 delivery dates with most open orders',
        'Returns the top 3 delivery dates with the most orders where the status is not ''completed''.',
        true,
        'SELECT count(1) as open_orders, delivery_date FROM operations.orders where status != ''COMPLETED'' group by 2 order by 1 desc limit 3',
        CURRENT_TIMESTAMP(3)
    );
INSERT INTO analytical_platform.report_operations (
        report_id,
        report_description,
        report_long_description,
        enabled,
        query,
        updated_at
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_report_id_seq'::regclass
        ),
        'Amount of pending products.',
        'Returns the total amount of pending items in orders with a ''PENDING'' status, by product_id in decreasing order.',
        true,
        'SELECT p.product_name, p.product_id, SUM(oi.quanity) AS total_quantity FROM operations.orders o JOIN operations.order_items oi ON o.order_id = oi.order_id JOIN operations.products p ON p.product_id = oi.product_id WHERE o.status = ''PENDING'' GROUP BY p.product_id order by total_quantity desc',
        CURRENT_TIMESTAMP(3)
    );
INSERT INTO analytical_platform.report_operations (
        report_id,
        report_description,
        report_long_description,
        enabled,
        query,
        updated_at
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_report_id_seq'::regclass
        ),
        'Clients with the most pending orders.',
        'Returns the three clients with the most amount of pending orders, regardless if they are active.',
        true,
        'select count(1) as pending_orders, c.customer_id, c.customer_name, c.is_active  from operations.customers c join operations.orders o on o.customer_id = c.customer_id join operations.order_items oi on oi.order_id = o.order_id where o.status = ''PENDING'' group by c.customer_id order by 1 desc limit 3',
        CURRENT_TIMESTAMP(3)
    );


INSERT INTO analytical_platform.report_operations (
        report_id,
        report_description,
        report_long_description,
        enabled,
        query,
        updated_at,
        argument_usage
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_report_id_seq'::regclass
        ),
        'N Clients with the most orders with a given status.',
        'Returns specified amount of clients with the most amount of orders with the given status.',
        true,
        'select count(1) as orders, c.customer_id, c.customer_name, c.is_active, o.status from operations.customers c join operations.orders o on o.customer_id = c.customer_id join operations.order_items oi on oi.order_id = o.order_id {where} group by c.customer_id, o.status order by 1 desc limit {limit}',
        CURRENT_TIMESTAMP(3),
        ' 10000 ''2025-02-25'''
    );
INSERT INTO analytical_platform.report_operations_arguments (
        argument_id,
        report_id,
        argument_name,
        argument_description,
        embedded,
        optional,
        block,
        example,
        updated_at,
        argument_position
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_arguments_argument_id_seq'::regclass
        ),
        (
            select report_id
            from analytical_platform.report_operations ao
            where report_description = 'N Clients with the most orders with a given status.'
        ),
        'limit',
        'Amount of rows to return.',
        true,
        false,
        null,
        '1000',
        CURRENT_TIMESTAMP(3),
        0
    );
INSERT INTO analytical_platform.report_operations_arguments (
        argument_id,
        report_id,
        associated_field,
        argument_name,
        argument_description,
        embedded,
        optional,
        block,
        example,
        updated_at,
        argument_position
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_arguments_argument_id_seq'::regclass
        ),
        (
            select report_id
            from analytical_platform.report_operations ao
            where report_description = 'N Clients with the most orders with a given status.'
        ),
        'o.status',
        'order-status',
        'Specific status to filter.',
        false,
        true,
        'where',
        'COMPLETED, PENDING, PROCESSING, REPROCESSING',
        CURRENT_TIMESTAMP(3),
        1
    );
INSERT INTO analytical_platform.report_operations
(
    report_id,
    report_description,
    report_long_description,
    enabled,
    query,
    updated_at,
    argument_usage
)
VALUES(
        nextval(
            'analytical_platform.report_operations_report_id_seq'::regclass
        ),
        'Orders filtered by status and delivery date.',
        'A more flexible order count report that can be filtered by status and delivery date.',
        true,
        'select count(1) as orders, c.customer_id, o.status, c.customer_name, o.delivery_date, c.is_active from operations.customers c join operations.orders o on o.customer_id = c.customer_id join operations.order_items oi on oi.order_id = o.order_id {where} group by c.customer_id, o.delivery_date, o.status  order by 1 desc',
        CURRENT_TIMESTAMP(3),
        '''2025-02-25'' ''PROCESSED'''
    );
INSERT INTO analytical_platform.report_operations_arguments (
        argument_id,
        report_id,
        associated_field,
        argument_name,
        argument_description,
        embedded,
        optional,
        block,
        example,
        updated_at,
        argument_position
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_arguments_argument_id_seq'::regclass
        ),
        (
            select report_id
            from analytical_platform.report_operations ao
            where report_description = 'Orders filtered by status and delivery date.'
        ),
        'o.delivery_date',
        'delivery-date',
        'Specific delivery date to filter.',
        false,
        true,
        'where',
        '2025-02-25',
        CURRENT_TIMESTAMP(3),
        0
    );
INSERT INTO analytical_platform.report_operations_arguments (
        argument_id,
        report_id,
        associated_field,
        argument_name,
        argument_description,
        embedded,
        optional,
        block,
        example,
        updated_at,
        argument_position
    )
VALUES(
        nextval(
            'analytical_platform.report_operations_arguments_argument_id_seq'::regclass
        ),
        (
            select report_id
            from analytical_platform.report_operations ao
            where report_description = 'Orders filtered by status and delivery date.'
        ),
        'o.status',
        'order-status',
        'Specific status to filter.',
        false,
        true,
        'where',
        'COMPLETED, PENDING, PROCESSING, REPROCESSING',
        CURRENT_TIMESTAMP(3),
        1
    );