# GitHub Account Management Guide

## Current Setup Analysis

You have two GitHub accounts:
- **Personal**: `Guidosalimbeni` 
- **Business**: `iagl-guido-salimbeni` (associated with guido.salimbeni@avios.com)

## What Happened

1. Your Git global config uses your business email, so GitHub authenticated you as your business account
2. When you tried to push to your personal repo, GitHub created a fork in your business account
3. This is normal behavior when you don't have write access to the original repo

## Current Configuration

### SSH Keys Setup ✅
```
~/.ssh/config:
- Default (Personal): Uses id_rsa for github.com
- Business: Uses id_ed25519_guido_iagl for github-guido-iagl
```

### Remote URLs (Now Fixed) ✅
```
origin: git@github-guido-iagl:iagl-guido-salimbeni/SmeHub_api.git (business fork)
upstream: git@github.com:Guidosalimbeni/SmeHub_api.git (personal original)
```

## How to Work with Multiple Accounts

### Method 1: Repository-Specific Git Config (Recommended)

For personal projects, override the global config locally:

```bash
# In your personal repo directory
git config user.name "Guidosalimbeni"
git config user.email "your-personal-email@gmail.com"
```

For business projects, the global config will be used automatically.

### Method 2: Directory-Based Config

Create separate directories and use conditional includes in your global Git config:

```bash
# Add to ~/.gitconfig
[includeIf "gitdir:~/Documents/personal/"]
    path = ~/.gitconfig-personal

[includeIf "gitdir:~/Documents/work/"]
    path = ~/.gitconfig-work
```

Then create `~/.gitconfig-personal`:
```
[user]
    name = Guidosalimbeni
    email = your-personal-email@gmail.com
```

## Workflow for This Repository

### Current State
- `origin` → Your business fork (where you can push)
- `upstream` → Your personal original repo

### Typical Workflow
1. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "Your changes"
   ```

2. **Push to your business fork**:
   ```bash
   git push origin main
   ```

3. **Create PR from business fork to personal repo** via GitHub web interface

4. **Sync with personal repo**:
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

## Quick Account Switching Commands

### Check current config:
```bash
git config user.name
git config user.email
```

### Switch to personal account (for current repo):
```bash
git config user.name "Guidosalimbeni"
git config user.email "your-personal-email@gmail.com"
```

### Switch to business account (for current repo):
```bash
git config user.name "Guidosalimbeni"
git config user.email "guido.salimbeni@avios.com"
```

## SSH Key Testing

Test your SSH connections:

```bash
# Test personal account
ssh -T git@github.com

# Test business account  
ssh -T git@github-guido-iagl
```

## Best Practices

1. **Keep business and personal work separate**
2. **Use SSH URLs** (not HTTPS) to leverage your SSH key setup
3. **Set repository-specific configs** for personal projects
4. **Always verify your identity** before committing:
   ```bash
   git config user.email
   ```

## Troubleshooting

If you get permission errors:
1. Check which account you're using: `git config user.email`
2. Verify SSH connection: `ssh -T git@github.com` or `ssh -T git@github-guido-iagl`
3. Ensure you're pushing to the correct remote (origin vs upstream)

## Security Note

Your current setup is secure:
- SSH keys are properly separated
- Business credentials remain intact
- You can work on personal projects without affecting company setup
