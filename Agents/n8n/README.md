# Daily WhatsApp Business message

Import `daily-whatsapp-template.json` into n8n. This workflow sends one approved WhatsApp Business template to one number every day at 9:00 AM India time. It is inactive by default.

## Configure it

1. In the **Send WhatsApp template** node, create and select an **HTTP Header Auth** credential with header name `Authorization` and value `Bearer <your WhatsApp Cloud API access token>`.
2. Replace `REPLACE_WITH_PHONE_NUMBER_ID` in the request URL with the Phone Number ID from your WhatsApp Business account.
3. Edit the request body and replace `REPLACE_WITH_RECIPIENT_NUMBER` with the recipient's number in international format, without a `+`.
4. Replace `REPLACE_WITH_APPROVED_TEMPLATE_NAME` and set the template language code to match an approved template in your WhatsApp Business account.
5. Test the workflow, then activate it. It will send once per day at 9:00 AM in `Asia/Kolkata`; change the schedule or workflow timezone if needed.

The recipient and template are fixed in the node. Proactive scheduled messages must use an approved template. This workflow requires the WhatsApp Business Cloud API; it does not connect to a personal WhatsApp account. Keep the access token in n8n credentials, not in the workflow JSON.
