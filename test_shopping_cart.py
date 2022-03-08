import unittest
from cofi_code import  CheckoutClass

class TestCheckout(unittest.TestCase):
    @staticmethod
    def importChekout():
        co = CheckoutClass("prices.json","discounts.json")
        return co

    def testScan(self):
        co = self.importChekout()
        co.scan("VOUCHER")
        co.scan("VOUCHER")
        co.scan("VOUCHER")
        testDict = {'VOUCHER': 3, 'TSHIRT': 0, 'MUG': 0}
        self.assertTrue(co.scannedItems == testDict, "Error: scanned items "
                                                     "doesnt correspond with "
                                                     "values on testDict.")

    def testGetItemNames(self):
        co = self.importChekout()
        itemNames = co._getItemsNames()
        dctNames = {'VOUCHER': 0, 'TSHIRT': 0, 'MUG': 0}
        self.assertTrue(itemNames == dctNames, "Error: function _getItemNames "
                                               "is not working properly")

    def testDiscountSwag(self):
        co = self.importChekout()
        for i in range(2):
            co.scan("VOUCHER")
            co.scan("TSHIRT")
            co.scan("MUG")
        emptyList, total = co._applyDiscounts()
        self.assertTrue(total == 50, "Error in function _applyDiscounts: "
                                     " swag discount is not working")
        self.assertTrue(emptyList == [0,0,0], "Error in function "
                                              "_applyDiscounts: remaining items"
                                              "list is not [0,0,0]")

    def testDiscount2for1(self):
        co = self.importChekout()
        for i in range(5):
            co.scan("VOUCHER")
        emptyList, total = co._applyDiscounts()
        self.assertTrue(total == 10, "Error in function _applyDiscounts: "
                                     " 2for1 discount is not working")
        self.assertTrue(emptyList == [1,0,0], "Error in function "
                                              "_applyDiscounts: remaining items"
                                              "list is not [1,0,0]")
    def testDiscountbulky(self):
        co = self.importChekout()
        c = 4
        for i in range(c):
            co.scan("TSHIRT")
        emptyList, total = co._applyDiscounts()
        value = 19 * c
        self.assertTrue(total == value, "Error in function _applyDiscounts: "
                                     " bulky discount is not working,"
                                        "value: %0.2f" % value)
        self.assertTrue(emptyList == [0,0,0], "Error in function "
                                              "_applyDiscounts: remaining items"
                                              "list is not [0,0,0]")

    def testTotal(self):
        co = self.importChekout()
        co.scan("VOUCHER")
        co.scan("MUG")
        trueValue = "total amount: 12.50 €"
        self.assertTrue(co.total() == trueValue, "Funtion total failed. The "
                                                 "total amount not correspond"
                                                 "to expected value.")

if __name__ == '__main__':
    unittest.main()


