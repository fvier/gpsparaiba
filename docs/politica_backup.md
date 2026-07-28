# 🛡️ Política de Backup 3-2-1 (Rastrek)

Regras e estratégias de backup para garantir a resiliência e integridade dos dados da plataforma **Rastrek**.

---

## 1. Regra 3-2-1
- **3 Cópias de dados**: 1 cópia em produção + 2 cópias de backup.
- **2 Meios de armazenamento diferentes**: Disco local / NAS + Nuvem.
- **1 Cópia Offsite**: Backup criptografado enviado para provedor de nuvem (ex: AWS S3 ou Rclone offsite).

---

## 2. Frequência de Backups
- **Banco de Dados**: Snapshots diários completos e logs incrementais.
- **Arquivos de Configuração & Código**: Versionamento contínuo via repositório Git.
