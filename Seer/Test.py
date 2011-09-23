class VisionTest:
    test_type = ""
    roi_code = ""
    test_code = ""

    def __init__(self, testtype, roisource, testsource):
	self.test_type = testtype
        self.roi_code = compile(roisource, "<string>", "exec")
        self.test_code = compile(testsource, "<string>", "exec")

    def exec(image, roiorigin = (), roidims = ())
	if (roiorigin != ()):
		roiorigin,
	


        
