const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGO_URI;

// ── PRICING TIERS ──
function getRate(buyerType, totalNights) {
  const tiers = {
    city:  [4.50, 3.00, 2.25],
    state: [4.00, 2.60, 1.90],
    ngo:   [2.50, 1.60, 1.25]
  };
  const rates = tiers[buyerType] || tiers.city;
  const i = totalNights <= 500 ? 0 : totalNights <= 10000 ? 1 : 2;
  return rates[i];
}

function getLeaseRate(buyerType) {
  const rates = { city: 210, state: 210, ngo: 126 };
  return rates[buyerType] || 210;
}

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid JSON' }) };
  }

  const client = new MongoClient(MONGO_URI);

  try {
    await client.connect();
    const db = client.db('encounter_db');

    // ── EXISTING ACTIONS ──

    if (body.action === 'signup') {
      const existing = await db.collection('users').findOne({ email: body.email });
      if (existing) {
        return { statusCode: 409, headers, body: JSON.stringify({ error: 'Email already exists' }) };
      }
      await db.collection('users').insertOne({
        first_name: body.first_name,
        last_name: body.last_name,
        organization: body.organization,
        email: body.email,
        role: body.role,
        created_at: new Date()
      });
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, message: 'Account created' }) };
    }

    if (body.action === 'register_device') {
      await db.collection('devices').insertOne({
        device_name: body.device_name,
        serial_id: body.serial_id,
        cluster_zone: body.cluster_zone,
        device_type: body.device_type,
        deployment_site: body.deployment_site,
        city_region: body.city_region,
        country: body.country,
        latitude: body.latitude,
        longitude: body.longitude,
        elevation: body.elevation,
        solar_panel_w: body.solar_panel_w,
        ice_target_kg: body.ice_target_kg,
        threshold_alert: body.threshold_alert,
        triage_intelligence: body.triage_intelligence,
        technician_notes: body.technician_notes,
        created_at: new Date()
      });
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, message: 'Device registered' }) };
    }

    if (body.action === 'add_stakeholder') {
      await db.collection('stakeholders').insertOne({
        id: 'SH-' + Date.now(),
        name: body.name,
        type: body.type,
        icon: body.icon,
        contact_name: body.contact_name,
        contact_email: body.contact_email,
        contact_phone: body.contact_phone,
        linked_devices: body.linked_devices,
        delivery: body.delivery,
        status: 'active',
        subscriptions: body.subscriptions,
        created_at: new Date()
      });
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, message: 'Stakeholder added' }) };
    }

    if (body.action === 'login') {
      const user = await db.collection('users').findOne({ email: body.email });
      if (!user) {
        return { statusCode: 401, headers, body: JSON.stringify({ error: 'No account found with that email' }) };
      }
      if (user.password !== body.password) {
        return { statusCode: 401, headers, body: JSON.stringify({ error: 'Incorrect password' }) };
      }
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, first_name: user.first_name, email: user.email, role: user.role }) };
    }

    if (body.action === 'get_records') {
      const records = await db.collection(body.collection).find({}).sort({ created_at: -1 }).toArray();
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, records }) };
    }

    // ── BILLING ACTIONS ──

    // Create a subscription when a customer signs a contract
    if (body.action === 'create_subscription') {
      const existing = await db.collection('subscriptions').findOne({ customer_id: body.customer_id });
      if (existing) {
        return { statusCode: 409, headers, body: JSON.stringify({ error: 'Subscription already exists for this customer' }) };
      }
      await db.collection('subscriptions').insertOne({
        customer_id: body.customer_id,       // e.g. 'phoenix-maricopa-001'
        customer_name: body.customer_name,   // e.g. 'City of Phoenix'
        buyer_type: body.buyer_type,         // 'city' | 'state' | 'ngo'
        unit_count: body.unit_count,         // number of Sentinel units deployed
        contract_start: new Date(body.contract_start),
        contract_end: body.contract_end ? new Date(body.contract_end) : null,
        status: 'active',
        created_at: new Date()
      });
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, message: 'Subscription created' }) };
    }

    // Log a cooling night event from a Sentinel unit
    if (body.action === 'log_cooling_night') {
      const now = new Date();
      await db.collection('cooling_events').insertOne({
        customer_id: body.customer_id,
        device_id: body.device_id,
        ambient_temp: body.ambient_temp,
        location: body.location || null,
        event_date: body.event_date ? new Date(body.event_date) : now,
        month_key: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`,
        created_at: now
      });
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, message: 'Cooling night logged' }) };
    }

    // Get current month usage + estimated cost for a customer
    if (body.action === 'get_usage') {
      const sub = await db.collection('subscriptions').findOne({ customer_id: body.customer_id });
      if (!sub) {
        return { statusCode: 404, headers, body: JSON.stringify({ error: 'No subscription found' }) };
      }
      const now = new Date();
      const month_key = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
      const events = await db.collection('cooling_events').countDocuments({
        customer_id: body.customer_id,
        month_key: month_key
      });
      const rate = getRate(sub.buyer_type, events);
      const lease = getLeaseRate(sub.buyer_type) * sub.unit_count;
      const platform_fee = events < 500 ? 0 : 1000;
      const estimated_total = Math.round(events * rate + lease + platform_fee);
      return {
        statusCode: 200, headers,
        body: JSON.stringify({
          ok: true,
          customer_id: body.customer_id,
          customer_name: sub.customer_name,
          buyer_type: sub.buyer_type,
          month: month_key,
          cooling_nights: events,
          rate_per_night: rate,
          unit_count: sub.unit_count,
          lease_total: lease,
          platform_fee: platform_fee,
          estimated_total: estimated_total
        })
      };
    }

    // Generate a monthly invoice for a customer
    if (body.action === 'generate_invoice') {
      const sub = await db.collection('subscriptions').findOne({ customer_id: body.customer_id });
      if (!sub) {
        return { statusCode: 404, headers, body: JSON.stringify({ error: 'No subscription found' }) };
      }
      const month_key = body.month_key; // e.g. '2026-06'
      const existing_invoice = await db.collection('invoices').findOne({
        customer_id: body.customer_id,
        month_key: month_key
      });
      if (existing_invoice) {
        return { statusCode: 409, headers, body: JSON.stringify({ error: 'Invoice already exists for this period' }) };
      }
      const events = await db.collection('cooling_events').countDocuments({
        customer_id: body.customer_id,
        month_key: month_key
      });
      const rate = getRate(sub.buyer_type, events);
      const lease = getLeaseRate(sub.buyer_type) * sub.unit_count;
      const platform_fee = events < 500 ? 0 : 1000;
      const amount_due = Math.round(events * rate + lease + platform_fee);
      const invoice = {
        invoice_id: 'INV-' + Date.now(),
        customer_id: body.customer_id,
        customer_name: sub.customer_name,
        buyer_type: sub.buyer_type,
        month_key: month_key,
        cooling_nights: events,
        rate_per_night: rate,
        unit_count: sub.unit_count,
        lease_total: lease,
        platform_fee: platform_fee,
        amount_due: amount_due,
        status: 'pending',
        created_at: new Date()
      };
      await db.collection('invoices').insertOne(invoice);
      return { statusCode: 200, headers, body: JSON.stringify({ ok: true, invoice }) };
    }

    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Unknown action' }) };

  } catch (err) {
    console.error('MongoDB error:', err);
    return { statusCode: 500, headers, body: JSON.stringify({ error: err.message }) };
  } finally {
    await client.close();
  }
};
