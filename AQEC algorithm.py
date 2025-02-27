import numpy as np
import random
import hashlib
import matplotlib.pyplot as plt

def generate_bits_and_bases(n):
    bits = np.random.randint(0, 2, n)  
    bases = np.random.choice(['+', 'x'], n) 
    return bits, bases

def measure_qubits(bits, send_bases, receive_bases):
    received_bits = []
    for bit, send_basis, receive_basis in zip(bits, send_bases, receive_bases):
        if send_basis == receive_basis:
            received_bits.append(bit)  
        else:
            received_bits.append(np.random.randint(0, 2))  
    return np.array(received_bits)

def sift_key(bits, send_bases, receive_bases):
    matching_indices = np.where(send_bases == receive_bases)[0]
    sifted_key = bits[matching_indices]
    return sifted_key, len(matching_indices) / len(bits)  

def eavesdrop(bits, bases, eavesdrop_rate=0.2):
    eavesdropped_bits = bits.copy()
    eavesdropped_bases = bases.copy()
    indices = np.random.choice(len(bits), int(eavesdrop_rate * len(bits)), replace=False)
    for i in indices:
        eavesdropped_bases[i] = random.choice(['+', 'x'])  
        if eavesdropped_bases[i] != bases[i]:
            eavesdropped_bits[i] = np.random.randint(0, 2)  
    return eavesdropped_bits, eavesdropped_bases

def error_correction(bits):
    corrected_bits = bits.copy()
    for i in range(0, len(bits) - 1, 2):
        if bits[i] != bits[i + 1]:
            corrected_bits[i] = corrected_bits[i + 1]  
    return corrected_bits

def bit_error_rate(original_bits, received_bits):
    errors = np.sum(original_bits != received_bits)
    return (errors / len(original_bits)) * 100  

def privacy_amplification(bits):
    bit_string = ''.join(map(str, bits))
    hashed = hashlib.sha256(bit_string.encode()).hexdigest()
    final_key = hashed[:len(bits)//2]  
    return final_key

def encrypt_message(message, key):
    key_repeated = (key * (len(message) // len(key) + 1))[:len(message)]
    encrypted_message = ''.join(chr(ord(m) ^ ord(k)) for m, k in zip(message, key_repeated))
    return encrypted_message

def decrypt_message(encrypted_message, key):
    key_repeated = (key * (len(encrypted_message) // len(key) + 1))[:len(encrypted_message)]
    decrypted_message = ''.join(chr(ord(e) ^ ord(k)) for e, k in zip(encrypted_message, key_repeated))
    return decrypted_message

def visualize_results(barman_bits, radin_bits, eavesdropped_bits, skr, ber):
    plt.figure(figsize=(10, 5))
    plt.plot(barman_bits, 'go-', label="Barman’s Bits")
    plt.plot(radin_bits, 'bo-', label="Radin’s Bits")
    plt.plot(eavesdropped_bits, 'ro-', label="Eve’s Interception", alpha=0.5)
    
    plt.xlabel("Bit Index")
    plt.ylabel("Bit Value")
    plt.legend()
    plt.title("QKD with an Attempted Eavesdropping Attack")

    
    plt.figtext(0.15, 0.02, f"Secure Key Rate (SKR): {skr:.2f} bits/qubit", fontsize=12, color="blue")
    plt.figtext(0.15, 0.05, f"Quantum Bit Error Rate (QAABER): {ber:.2f}%", fontsize=12, color="red")

    plt.show()

def main():
    n = 100  
    barman_bits, barman_bases = generate_bits_and_bases(n)
    eavesdropped_bits, eavesdropped_bases = eavesdrop(barman_bits, barman_bases, eavesdrop_rate=0.2)
    radin_bases = np.random.choice(['+', 'x'], n)
    radin_bits = measure_qubits(eavesdropped_bits, eavesdropped_bases, radin_bases)
    
    sifted_key, skr = sift_key(radin_bits, eavesdropped_bases, radin_bases)
    ber = bit_error_rate(barman_bits[:len(sifted_key)], sifted_key) 
    
    corrected_key = error_correction(sifted_key)
    final_key = privacy_amplification(corrected_key)
        
    print(f'Final Secure Key: {final_key}')
    print(f'Secure Key Rate (SKR): {skr:.2f} bits/qubit')
    print(f'Bit Error Rate (BER): {ber:.2f}%')
    
    
    message1 = input("Enter first message: ")
    message2 = input("Enter second message: ")
    
    encrypted_message1 = encrypt_message(message1, final_key)
    encrypted_message2 = encrypt_message(message2, final_key)
    decrypted_message1 = decrypt_message(encrypted_message1, final_key)
    decrypted_message2 = decrypt_message(encrypted_message2, final_key)
    
    print(f'Encrypted Message 1: {encrypted_message1}')
    print(f'Decrypted Message 1: {decrypted_message1}')
    print(f'Encrypted Message 2: {encrypted_message2}')
    print(f'Decrypted Message 2: {decrypted_message2}')
    
    visualize_results(barman_bits, radin_bits, eavesdropped_bits, skr, ber)

if __name__ == "__main__":
    main()
