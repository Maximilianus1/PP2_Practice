CREATE OR REPLACE PROCEDURE upsert_contact(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE username = p_username) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO contacts(username, phone)
        VALUES(p_username, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1)
    LOOP
        IF p_phones[i] ~ '^+7[0-9]{10}$' THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %, name: %', p_phones[i], p_names[i];
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE username = p_value OR phone = p_value;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phones (contact_id, phone, type)
    VALUES (
        (SELECT id FROM contacts WHERE username = p_contact_name),
        p_phone,
        p_type
    );
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    UPDATE contacts
    SET group_id = (SELECT id FROM groups WHERE name = p_group_name)
    WHERE username = p_contact_name;
END;
$$;