# from web3 import Web3

# # Connect to blockchain (Ethereum, Polygon, or a private chain)
# WEB3_PROVIDER = "https://polygon-mumbai.infura.io/v3/0f1fde990b6546089035da7e1b6907ca"
# web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

# # Smart contract details
# CONTRACT_ADDRESS = "0xYourSmartContractAddress"
# CONTRACT_ABI = [...]  # Paste your contract ABI here

# contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
import hashlib
from .models import BlockchainRecord,News

def generate_content_hash(news):
    """
    Generates a SHA-256 hash based on news content and media URLs.
    """
    try:
        # Access URLs safely
        photo_url = news.photo.url if news.photo and hasattr(news.photo, 'url') else ''
        video_url = news.video.url if news.video and hasattr(news.video, 'url') else ''

        # Create hash input
        hash_input = f"{news.content}{photo_url}{video_url}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    except Exception as e:
        print(f"❌ Error in generate_content_hash: {e}")
        return None


def store_on_blockchain(news, content_hash):
    """
    Stores hash in the BlockchainRecord model instead of blockchain.
    """
    try:
        if not isinstance(news, News):
            raise ValueError("Expected a News object, but got something else.")

        # Save the hash in BlockchainRecord (Create or Update)
        blockchain_record, created = BlockchainRecord.objects.update_or_create(
            news=news,
            defaults={"content_hash": content_hash}
        )

        print(f"✅ Hash Stored: {content_hash} (Created: {created})")
        return content_hash  # Simulated blockchain transaction ID

    except Exception as e:
        print(f"❌ Error in store_on_blockchain: {e}")
        return None


def verify_blockchain_hash(news):
    """
    Compares the stored hash in BlockchainRecord with a newly generated hash.
    """
    try:
        # Fetch stored record
        stored_record = BlockchainRecord.objects.get(news=news)

        # Generate new hash from current content
        current_hash = generate_content_hash(news)

        # Compare stored and current hash
        is_valid = stored_record.content_hash == current_hash
        print(f"🔍 Verification: {'Valid' if is_valid else 'Tampered'}")
        return is_valid

    except BlockchainRecord.DoesNotExist:
        print("❌ No blockchain record found! Possible tampering.")
        return False
    except Exception as e:
        print(f"❌ Error in verify_blockchain_hash: {e}")
        return False