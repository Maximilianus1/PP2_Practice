CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.username, c.phone
    FROM contacts c
    WHERE c.username ILIKE '%' || p || '%'
       OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.username, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (username VARCHAR, phone VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR, phones JSON) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.username,
        c.phone,
        c.email,
        c.birthday,
        g.name as group_name,
        json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.username ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;