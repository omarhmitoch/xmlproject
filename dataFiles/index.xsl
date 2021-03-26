<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" omit-xml-declaration="yes" />
<xsl:template match="/">
        
       <div class="familytree" data-name="{familytree/@familyName}">
                    <xsl:for-each select="familytree">
                        <xsl:for-each select="generation">
                        <div class="generation">
                        <ul>
                             <xsl:for-each select="personne">
                                <xsl:choose>
                                <xsl:when test="contains(@estroi,'True')">
                                  <li id="king"> <i class="fas fa-crown"></i><span><xsl:value-of select="nomcomplet"/></span></li>
                                </xsl:when>
                                <xsl:otherwise>
                                  <li><span><xsl:value-of select="nomcomplet"/></span></li>
                                </xsl:otherwise>
                              </xsl:choose>
                            </xsl:for-each>
                            </ul>
                        </div>
                        </xsl:for-each>
                    </xsl:for-each>
        </div>
 
</xsl:template>
</xsl:stylesheet>