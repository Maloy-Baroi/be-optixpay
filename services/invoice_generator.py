def generate_invoice_number():
    fixed_part = "MCNTInv"  # Fixed part (11 characters)
    sequential_number = 1  # Starting number (you can increment this dynamically or based on your logic)

    # Generate the number part with leading zeros to make it 15 characters in total
    invoice_number = f"{fixed_part}{str(sequential_number).zfill(8)}"
    
    return invoice_number