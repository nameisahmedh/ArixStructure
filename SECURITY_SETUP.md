# Security Setup Instructions

## 1. Set up your Hugging Face Token

### Option A: Using secrets.toml (Recommended for local development)
1. Copy your HF token
2. Edit `.streamlit/secrets.toml`:
   ```toml
   HF_TOKEN = "your_actual_token_here"
   ```

### Option B: Using Environment Variables (Recommended for production)
1. Create a `.env` file in the project root:
   ```
   HF_TOKEN=your_actual_token_here
   ```
2. Or set the environment variable directly:
   ```bash
   export HF_TOKEN=your_actual_token_here
   ```

## 2. Security Features Implemented

- ✅ API tokens are no longer hardcoded
- ✅ URL validation prevents SSRF attacks
- ✅ Request timeouts and size limits
- ✅ Private/local IP blocking
- ✅ Better error handling
- ✅ Gitignore prevents token commits

## 3. Important Notes

- Never commit your actual tokens to version control
- The `.gitignore` file prevents accidental commits
- URL fetching is now restricted to public domains only
- File size limits prevent resource exhaustion

## 4. Testing

After setup, test the application:
1. Upload a document via Dashboard
2. Try the AI Assistant features
3. Verify URL fetching works with public URLs only