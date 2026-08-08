# remote-gui

`remote-gui` launches graphical Linux applications on a remote machine over SSH/X11 while isolating the application's D-Bus and XDG runtime environment.

It was originally created to work around GTK/Tilix hangs caused by remote applications interacting with an existing desktop session's:

- D-Bus session
- `XDG_RUNTIME_DIR`
- GVfs
- `xdg-desktop-portal`

Example:

```bash
remote-gui run spectrix xclock
remote-gui run spectrix gedit
remote-tilix spectrix
```

## Requirements

Both the local and remote machines should have OpenSSH installed.

On Ubuntu:

```bash
sudo apt install openssh-client
```

The remote machine must also run an SSH server:

```bash
sudo apt install openssh-server
sudo systemctl enable --now ssh
```

For X11 forwarding, install `xauth` on the remote machine:

```bash
sudo apt install xauth
```

`remote-gui` also expects the remote system to provide:

```text
bash
mktemp
dbus-run-session
```

You can check a configured host with:

```bash
remote-gui doctor HOST
```

---

# Configuring SSH

`remote-gui` deliberately uses your existing OpenSSH configuration instead of maintaining a separate host database.

SSH aliases are normally defined in:

```text
~/.ssh/config
```

## Important: SSH keys are directional

If machine **A** needs to SSH into machine **B**:

```text
Machine A                          Machine B

~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub  ----------> ~/.ssh/authorized_keys
```

The **public key from the machine initiating the SSH connection** must be installed in the destination machine's `authorized_keys`.

For bidirectional SSH, repeat the process in the opposite direction.

---

# Example: alienware -> spectrix

The following steps are performed on **alienware** unless otherwise specified.

## 1. Create an Ed25519 SSH key

First check whether one already exists:

```bash
ls -l ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub
```

If not, create one:

```bash
ssh-keygen -t ed25519
```

The default location is:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

Do not copy or share the private key:

```text
~/.ssh/id_ed25519
```

Only the `.pub` file should be copied to another machine.

## 2. Install alienware's public key on spectrix

From **alienware**:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub mora@192.168.1.125
```

Replace the username and IP address as appropriate.

The public key will be added to this file on **spectrix**:

```text
~/.ssh/authorized_keys
```

## 3. Create an SSH alias on alienware

Edit:

```bash
nano ~/.ssh/config
```

Add:

```text
Host spectrix
    HostName 192.168.1.125
    User mora
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ForwardX11 yes
    ForwardX11Trusted yes
```

Set safe permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
```

Test:

```bash
ssh spectrix
```

Then test X11 forwarding:

```bash
ssh -Y spectrix xclock
```

If an `xclock` window appears on alienware, X11 forwarding is working.

---

# Example: spectrix -> alienware

For SSH in the other direction, repeat the same process.

On **spectrix**, create or verify its own key:

```bash
ls -l ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub
```

If needed:

```bash
ssh-keygen -t ed25519
```

Copy **spectrix's public key** to alienware:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub mora@ALIENWARE_IP
```

Then edit `~/.ssh/config` on **spectrix**:

```text
Host alienware
    HostName ALIENWARE_IP
    User mora
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ForwardX11 yes
    ForwardX11Trusted yes
```

Test from spectrix:

```bash
ssh alienware
```

Then:

```bash
ssh -Y alienware xclock
```

---

# Verifying public-key authentication

To confirm which key SSH is using:

```bash
ssh -vvv spectrix
```

Look for:

```text
Offering public key: /home/USER/.ssh/id_ed25519
Server accepts key: /home/USER/.ssh/id_ed25519
Authenticated to ... using "publickey".
```

You can also force the Ed25519 key:

```bash
ssh \
    -i ~/.ssh/id_ed25519 \
    -o IdentitiesOnly=yes \
    spectrix
```

To make the test fail instead of falling back to a login password:

```bash
ssh \
    -i ~/.ssh/id_ed25519 \
    -o IdentitiesOnly=yes \
    -o PasswordAuthentication=no \
    spectrix
```

---

# Key passphrases and ssh-agent

There are two different prompts that are easy to confuse.

This:

```text
mora@spectrix's password:
```

is the password for the remote account.

This:

```text
Enter passphrase for key '/home/mora/.ssh/id_ed25519':
```

is the passphrase protecting your local private key.

Using `ssh-agent` allows you to enter the key passphrase once per login session.

Check loaded keys:

```bash
ssh-add -l
```

Add your Ed25519 key:

```bash
ssh-add ~/.ssh/id_ed25519
```

Then:

```bash
ssh spectrix
```

should use the key stored in the agent.

---

# SSH file permissions

If OpenSSH refuses to use `authorized_keys`, verify permissions on the destination machine:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

On the client:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

Never make the private key publicly readable.

---

# Testing remote-gui

Once SSH and X11 forwarding work normally:

```bash
ssh -Y spectrix xclock
```

test `remote-gui`:

```bash
remote-gui doctor spectrix
```

Then:

```bash
remote-gui run spectrix xclock
```

Tilix can be launched with:

```bash
remote-tilix spectrix
```

or:

```bash
remote-gui run spectrix tilix --new-process
```

For the reverse direction:

```bash
remote-gui doctor alienware
remote-tilix alienware
```

---

# Listing configured hosts

`remote-gui` reads SSH aliases from the local machine's:

```text
~/.ssh/config
```

List them with:

```bash
remote-gui hosts
```

Remember that SSH configurations are local to each machine.

For example, `spectrix` might contain:

```text
Host alienware
```

while `alienware` might contain:

```text
Host spectrix
```

The two `~/.ssh/config` files do not automatically synchronize.

---

# Troubleshooting

## `Permission denied (publickey)`

Run:

```bash
ssh -vvv HOST
```

Check whether your desired key is offered and accepted.

Verify that the source machine's `.pub` key exists in the destination machine's:

```text
~/.ssh/authorized_keys
```

## `DISPLAY` is empty

Connect using trusted X11 forwarding:

```bash
ssh -Y HOST
```

Then:

```bash
echo "$DISPLAY"
```

It should normally contain something similar to:

```text
localhost:10.0
```

Test with:

```bash
xclock
```

## Tilix or another GTK application hangs

A normal SSH/X11 session can expose the remote graphical application to the existing desktop session's D-Bus, GVfs, portals, and `/run/user/$UID` runtime resources.

`remote-gui` works around this by launching the application with an isolated runtime environment and private D-Bus session.

Instead of:

```bash
ssh -Y spectrix tilix
```

use:

```bash
remote-tilix spectrix
```

or:

```bash
remote-gui run spectrix tilix --new-process
```

## Show exactly what remote-gui would execute

Use:

```bash
remote-gui run --dry-run spectrix xclock
```

For additional SSH diagnostics:

```bash
remote-gui run --debug spectrix xclock
```
