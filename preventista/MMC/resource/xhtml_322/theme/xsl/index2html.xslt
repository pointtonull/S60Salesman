<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns="http://www.w3.org/TR/REC-html40">
	
	<xsl:output method="html"/>
	
	<!-- ====================================================================== -->
	<!-- Root element -->
	<xsl:template match="topics">
		<html>
			<head>
				<title><xsl:value-of select="@title"/></title>
				<link rel="stylesheet" type="text/css" href="../../theme/css/help.css"/>
			</head>
			<body>
				<h1><xsl:value-of select="@title"/></h1>
				<ul>
					<xsl:apply-templates/>
				</ul>
			</body>
		</html>
	</xsl:template>
	
	<!-- ====================================================================== -->
	<!-- Root element -->
	<xsl:template match="topicref">
		<li>
			<a>
				<xsl:attribute name="href">
					<xsl:value-of select="@href"/>
				</xsl:attribute>
				<xsl:value-of select="@navtitle"/>
			</a>
		</li>
	</xsl:template>

	
</xsl:stylesheet>
