# **Anti-Ad AdGuard Rules**

## **Project Description**
This project implements a Python-based ad-blocking proxy server using the AdGuard rules provided by the Anti-Ad project. The `anti-ad-adguard.txt` file contains the latest ad-blocking rules, which are used to filter and block common ad and tracking requests.

---

## **File Details**

### **`anti-ad-adguard.txt`**
- **Source**: Cloned from the [Anti-Ad GitHub repository](https://github.com/privacy-protection-tools/anti-AD).
- **Purpose**: Contains the ad-blocking rules used by the proxy server.
- **Syntax**: Follows AdGuard filtering rule syntax.

### **`proxy.py`**
- A Python script implementing the following features:
  1. Loads rules from `anti-ad-adguard.txt`.
  2. Intercepts and blocks HTTP/HTTPS requests that match the ad-blocking rules.
  3. Provides logs and outputs for testing.

---

## **How to Use**

### **1. Install Dependencies**
```bash
git clone this project
```

### **2. Run the Proxy Server**
```bash
python proxy.py
```

### **3. Configure Your Browser**
- Set your browser’s proxy settings to `127.0.0.1:8888`.

### **4. Test the Proxy**
- Visit websites to check if ads and tracking requests are successfully blocked.

---

## **Notes**
- Ensure that the `anti-ad-adguard.txt` file is in the same directory as the script.
- This project is for **educational and learning purposes only**. Please adhere to applicable laws and regulations when using this tool.

---

## **References**
- [Anti-Ad GitHub Repository](https://github.com/privacy-protection-tools/anti-AD) - Source of the ad-blocking rules.

---

## **Future Improvements**
- Add dynamic updates for the rules list.
- Optimize the proxy server to handle high-concurrency traffic.

---

## **Contact**
If you have any questions or suggestions, feel free to contact me at ian980306@gmail.com.

---

Feel free to customize this further based on your specific needs or additional features!
